"""
qdrant_pdf_pipeline.py — PDF ingestion pipeline for Qdrant
===========================================================
What students learn:
  - How a real ingestion pipeline works: PDF → text → chunks → vectors → storage
  - Why we split text into chunks (LLMs and embedding models have token limits)
  - What "overlap" does: keeps context across chunk boundaries so meaning isn't lost
  - How Sentence-Transformers turns text into a list of floats (a vector / embedding)
  - How Qdrant stores a vector alongside a payload (the original text, metadata)
  - How to read vectors back out of Qdrant to prove they were stored

Pipeline flow (also shown in the Streamlit "📦 Qdrant PDF lab"):
  PDF bytes
    └─ extract_text_from_pdf()   → raw text string
         └─ chunk_text()         → list of overlapping text chunks
              └─ embed_texts()   → list of 384-dim float vectors (one per chunk)
                   └─ ingest_pdf_to_qdrant()
                        ├─ ensure_collection()   → create Qdrant collection if absent
                        └─ client.upsert()       → store vectors + payload in Qdrant

Run as CLI (reads QDRANT_URL / QDRANT_API_KEY from .env):
    python qdrant_pdf_pipeline.py path/to/file.pdf
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO

from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm


# ── Step 1: Split text into overlapping chunks ────────────────────────────────
def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """
    Slice raw text into fixed-size character windows with an overlap.

    Why overlap? The end of chunk N and the start of chunk N+1 share `overlap`
    characters so a sentence split across a boundary still has context in both chunks.
    Example with chunk_size=10, overlap=3:
      "abcdefghij klmnop" → ["abcdefghij", "hijklmnop", ...]
    """
    text = text.strip()
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    # Cap overlap so we always make forward progress (step > 0)
    overlap = max(0, min(overlap, chunk_size - 1))
    step = max(1, chunk_size - overlap)
    chunks: list[str] = []
    n = len(text)
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunks.append(text[start:end])
        if end >= n:
            break
        start += step
    return chunks


# ── Step 2: Extract raw text from a PDF ──────────────────────────────────────
def extract_text_from_pdf(source: str | Path | BinaryIO | bytes) -> str:
    """
    Read every page of a PDF and join the text with blank lines.
    Accepts a file path, an open file-like object, or raw bytes
    (Streamlit's file_uploader returns bytes via .getvalue()).
    """
    if isinstance(source, (str, Path)):
        reader = PdfReader(str(source))
    elif isinstance(source, bytes):
        # Wrap bytes in BytesIO so PdfReader can seek through it
        reader = PdfReader(BytesIO(source))
    else:
        reader = PdfReader(source)
    parts: list[str] = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    return "\n\n".join(parts)


# ── Step 3: Choose the embedding model ───────────────────────────────────────
def default_embed_model_name() -> str:
    # all-MiniLM-L6-v2 → 384-dimensional vectors; fast, good quality, ~80 MB download
    return "sentence-transformers/all-MiniLM-L6-v2"


def _load_encoder(model_name: str | None = None):
    """
    Download (first run only) and load the embedding model into memory.

    WHY a lazy / deferred import?
    ─────────────────────────────
    `sentence_transformers` pulls in PyTorch under the hood.  PyTorch is large
    (~500 MB) and slow to import.  If we put `from sentence_transformers import …`
    at the top of the file, *every* import of this module — including the tests
    that only test chunking — would pay that startup cost.  By placing the import
    *inside* this function, PyTorch only loads the moment we actually need to embed.

    WHAT SentenceTransformer does:
    ───────────────────────────────
    It wraps a pre-trained neural network (here: all-MiniLM-L6-v2).
    When you call  model.encode("some text")  it:
      1. Tokenises the sentence into sub-word pieces.
      2. Runs those tokens through ~6 transformer layers.
      3. Pools the layer outputs into a single fixed-length vector (384 floats).
    The resulting vector captures the *meaning* of the sentence so that
    similar sentences end up close together in the 384-dimensional space.

    FIRST RUN vs subsequent runs:
    ──────────────────────────────
    On the first call, SentenceTransformer downloads the model weights from
    Hugging Face (~80 MB) and caches them in ~/.cache/huggingface/.
    Every subsequent call just loads from that cache — no download needed.

    RETURN VALUE:
    ─────────────
    A tuple of (model_object, resolved_model_name_string) so callers know
    which model was actually used (useful when model_name=None and the default
    is picked for them).
    """
    from sentence_transformers import SentenceTransformer

    # Use the caller's choice, or fall back to the project default (all-MiniLM-L6-v2)
    name = model_name or default_embed_model_name()
    # SentenceTransformer(name) triggers the download / cache-load here
    return SentenceTransformer(name), name


# ── Step 4: Convert chunks to vectors ────────────────────────────────────────
def embed_texts(
    texts: list[str],
    model_name: str | None = None,
) -> tuple[list[list[float]], int, str]:
    """
    Run a list of text chunks through the embedding model.
    Returns: (list_of_vectors, dimension_size, model_name_used)

    Each vector is a list of floats — e.g. 384 floats for all-MiniLM-L6-v2.
    These floats encode the *meaning* of the text, not just keywords.
    """
    model, resolved = _load_encoder(model_name)
    if not texts:
        # Return empty list but still report the model's dimension for UI display
        dim = model.get_sentence_embedding_dimension()
        return [], dim, resolved
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return vectors.tolist(), int(vectors.shape[1]), resolved


# ── Data structure returned after a successful ingest ────────────────────────
@dataclass
class IngestResult:
    collection_name: str
    points_upserted: int       # how many chunks were stored
    vector_dim: int            # e.g. 384 for all-MiniLM-L6-v2
    model_name: str            # which embedding model was used
    points_preview: list[dict[str, Any]]  # first-K dims + text preview for the UI


# ── Qdrant collection helpers ─────────────────────────────────────────────────
def _collection_exists(client: QdrantClient, name: str) -> bool:
    # Check the list of collections without raising if the name is absent
    cols = client.get_collections().collections
    return any(c.name == name for c in cols)


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_dim: int,
    distance: qm.Distance = qm.Distance.COSINE,
) -> None:
    """
    Create the collection only if it doesn't already exist.
    We use COSINE distance because all-MiniLM-L6-v2 vectors are trained
    to be compared by angle (direction), not raw magnitude.
    """
    if _collection_exists(client, collection_name):
        return
    client.create_collection(
        collection_name=collection_name,
        # VectorParams tells Qdrant the shape of every vector it will store
        vectors_config=qm.VectorParams(size=vector_dim, distance=distance),
    )


# ── Step 6 (optional): Delete a collection for a clean demo re-run ───────────
def delete_qdrant_collection(
    *,
    qdrant_url: str,
    api_key: str | None,
    collection_name: str,
) -> str:
    """
    Drop an entire collection from Qdrant (all vectors + payloads removed).
    The next ingest will recreate it from scratch.
    Used by the Streamlit "Clear collection" button.
    """
    client = QdrantClient(url=qdrant_url, api_key=api_key)
    if not _collection_exists(client, collection_name):
        return f"Collection {collection_name!r} does not exist — nothing to delete."
    client.delete_collection(collection_name=collection_name)
    return f"Deleted collection {collection_name!r}. You can ingest again to recreate it."


# ── Step 5: Main ingest function — orchestrates the full pipeline ─────────────
def ingest_pdf_to_qdrant(
    pdf_source: str | Path | BinaryIO | bytes,
    *,
    qdrant_url: str = "http://localhost:6333",
    api_key: str | None = None,
    collection_name: str = "cohort_pdf_demo",
    chunk_size: int = 400,
    overlap: int = 50,
    embed_model: str | None = None,
    preview_dims: int = 12,
) -> IngestResult:
    """
    End-to-end: PDF → Qdrant.
    The `preview_dims` argument controls how many vector dimensions are included
    in the returned IngestResult for display in the Streamlit dataframe.
    """
    # 2 → extract text
    text = extract_text_from_pdf(pdf_source)
    # 3 → split into chunks
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    if not chunks:
        raise ValueError("No text extracted from PDF (empty or image-only?)")

    # 4 → embed: returns one 384-dim vector per chunk
    vectors, dim, model_name = embed_texts(chunks, model_name=embed_model)

    # Connect to Qdrant and ensure the collection exists
    client = QdrantClient(url=qdrant_url, api_key=api_key)
    ensure_collection(client, collection_name, dim)

    # Build PointStruct list — each point = one UUID + one vector + one payload dict
    points: list[qm.PointStruct] = []
    preview: list[dict[str, Any]] = []
    for i, (vec, chunk) in enumerate(zip(vectors, chunks)):
        # UUID ensures each point has a globally unique ID even across multiple ingests
        pid = str(uuid.uuid4())
        payload = {
            "chunk_index": i,
            # Store a short preview so we can display source text next to the vector
            "text_preview": chunk[:200] + ("…" if len(chunk) > 200 else ""),
            "char_len": len(chunk),
        }
        points.append(qm.PointStruct(id=pid, vector=vec, payload=payload))
        # preview is shown in the Streamlit dataframe after ingest
        preview.append(
            {
                "id": pid,
                "chunk_index": i,
                "dimensions": dim,
                # Show only the first `preview_dims` floats — the full vector is 384 values
                "vector_first_k": vec[:preview_dims],
                "text_preview": payload["text_preview"],
            }
        )

    # Single upsert call — Qdrant batches this internally
    client.upsert(collection_name=collection_name, points=points)

    return IngestResult(
        collection_name=collection_name,
        points_upserted=len(points),
        vector_dim=dim,
        model_name=model_name,
        points_preview=preview,
    )


# ── Scroll helper: read stored points (with full vectors) back out ────────────
def scroll_points_with_vectors(
    client: QdrantClient,
    collection_name: str,
    limit: int = 20,
    *,
    with_vectors: bool = True,
) -> list[dict[str, Any]]:
    """
    Retrieve up to `limit` points from Qdrant, including their raw vectors.
    Used by the "Scroll & show vectors" button — the teaching moment where
    students see the actual float values that represent their PDF text.
    """
    records, _next = client.scroll(
        collection_name=collection_name,
        limit=limit,
        with_payload=True,
        with_vectors=with_vectors,  # False would be faster but we need the numbers
    )
    out: list[dict[str, Any]] = []
    for r in records:
        vec = r.vector
        # Named vectors return a dict; unnamed return a plain list
        if isinstance(vec, dict):
            vec = next(iter(vec.values())) if vec else None
        out.append(
            {
                "id": r.id,
                "payload": r.payload or {},
                "vector": list(vec) if vec is not None else None,
                "dimensions": len(vec) if vec is not None else None,
            }
        )
    return out


# ── Vector summary helper ─────────────────────────────────────────────────────
def summarize_vector(vec: list[float] | None, head: int = 16) -> dict[str, Any]:
    """
    Return a display-friendly summary of a single vector:
      - head: the first `head` float values (enough to make it concrete)
      - l2_norm: the length of the vector (≈1.0 for normalized embeddings)
      - length: total number of dimensions (e.g. 384)
    """
    if not vec:
        return {"head": [], "l2_norm": None}
    h = min(head, len(vec))
    # L2 norm = √(Σ xᵢ²) — normalized embeddings have norm ≈ 1.0
    l2 = math.sqrt(sum(x * x for x in vec))
    return {"head": vec[:h], "l2_norm": l2, "length": len(vec)}


# ── CLI entry point ───────────────────────────────────────────────────────────
def main() -> None:
    """
    Run the full pipeline from the command line.
    Reads QDRANT_URL / QDRANT_API_KEY / QDRANT_COLLECTION from .env first,
    then lets --flags override any value for one-off demos.

    Example:
        python qdrant_pdf_pipeline.py my_slides.pdf
        python qdrant_pdf_pipeline.py my_slides.pdf --qdrant-url https://xxx:6333
    """
    import argparse
    import os

    from vector_db_env import load_vector_db_env

    # Load .env before argparse so defaults can come from env vars
    load_vector_db_env()

    parser = argparse.ArgumentParser(description="Ingest a PDF into Qdrant (HTTP API).")
    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument(
        "--qdrant-url",
        default=None,
        help="Override QDRANT_URL (default: from .env, else http://localhost:6333)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Override QDRANT_API_KEY (default: from .env)",
    )
    parser.add_argument(
        "--collection",
        default=None,
        help="Override QDRANT_COLLECTION (default: cohort_pdf_demo)",
    )
    parser.add_argument("--chunk-size", type=int, default=400)
    parser.add_argument("--overlap", type=int, default=50)
    parser.add_argument("--model", default=None, help="sentence-transformers model id")
    args = parser.parse_args()

    # CLI flag → env var → hard-coded fallback (priority order)
    q_url = args.qdrant_url or os.getenv("QDRANT_URL", "").strip() or "http://localhost:6333"
    q_key = args.api_key if args.api_key is not None else os.getenv("QDRANT_API_KEY", "").strip() or None
    q_coll = (args.collection or os.getenv("QDRANT_COLLECTION", "").strip() or "cohort_pdf_demo")

    result = ingest_pdf_to_qdrant(
        args.pdf,
        qdrant_url=q_url,
        api_key=q_key,
        collection_name=q_coll,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        embed_model=args.model,
    )
    print(f"Collection: {result.collection_name}")
    print(f"Points: {result.points_upserted}  |  dim: {result.vector_dim}  |  model: {result.model_name}")
    for row in result.points_preview[:5]:
        print(row)
    if len(result.points_preview) > 5:
        print(f"... and {len(result.points_preview) - 5} more")


if __name__ == "__main__":
    main()

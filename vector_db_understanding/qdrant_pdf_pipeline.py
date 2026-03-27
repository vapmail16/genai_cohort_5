"""PDF → chunks → embeddings → Qdrant (HTTP API) with inspectable vectors."""

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


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks (character-based)."""
    text = text.strip()
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
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


def extract_text_from_pdf(source: str | Path | BinaryIO | bytes) -> str:
    """Read all pages from a PDF and concatenate extracted text."""
    if isinstance(source, (str, Path)):
        reader = PdfReader(str(source))
    elif isinstance(source, bytes):
        reader = PdfReader(BytesIO(source))
    else:
        reader = PdfReader(source)
    parts: list[str] = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    return "\n\n".join(parts)


def default_embed_model_name() -> str:
    return "sentence-transformers/all-MiniLM-L6-v2"


def _load_encoder(model_name: str | None = None):
    from sentence_transformers import SentenceTransformer

    name = model_name or default_embed_model_name()
    return SentenceTransformer(name), name


def embed_texts(
    texts: list[str],
    model_name: str | None = None,
) -> tuple[list[list[float]], int, str]:
    """Return list of vectors, embedding dimension, and resolved model name."""
    model, resolved = _load_encoder(model_name)
    if not texts:
        dim = model.get_sentence_embedding_dimension()
        return [], dim, resolved
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return vectors.tolist(), int(vectors.shape[1]), resolved


@dataclass
class IngestResult:
    collection_name: str
    points_upserted: int
    vector_dim: int
    model_name: str
    points_preview: list[dict[str, Any]]


def _collection_exists(client: QdrantClient, name: str) -> bool:
    cols = client.get_collections().collections
    return any(c.name == name for c in cols)


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_dim: int,
    distance: qm.Distance = qm.Distance.COSINE,
) -> None:
    if _collection_exists(client, collection_name):
        return
    client.create_collection(
        collection_name=collection_name,
        vectors_config=qm.VectorParams(size=vector_dim, distance=distance),
    )


def delete_qdrant_collection(
    *,
    qdrant_url: str,
    api_key: str | None,
    collection_name: str,
) -> str:
    """
    Drop the collection so the next ingest recreates it (empty slate).
    """
    client = QdrantClient(url=qdrant_url, api_key=api_key)
    if not _collection_exists(client, collection_name):
        return f"Collection {collection_name!r} does not exist — nothing to delete."
    client.delete_collection(collection_name=collection_name)
    return f"Deleted collection {collection_name!r}. You can ingest again to recreate it."


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
    Extract PDF → chunk → embed → upsert to Qdrant.
    Uses Qdrant HTTP API (QdrantClient).
    """
    text = extract_text_from_pdf(pdf_source)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    if not chunks:
        raise ValueError("No text extracted from PDF (empty or image-only?)")

    vectors, dim, model_name = embed_texts(chunks, model_name=embed_model)
    client = QdrantClient(url=qdrant_url, api_key=api_key)
    ensure_collection(client, collection_name, dim)

    points: list[qm.PointStruct] = []
    preview: list[dict[str, Any]] = []
    for i, (vec, chunk) in enumerate(zip(vectors, chunks)):
        pid = str(uuid.uuid4())
        payload = {
            "chunk_index": i,
            "text_preview": chunk[:200] + ("…" if len(chunk) > 200 else ""),
            "char_len": len(chunk),
        }
        points.append(qm.PointStruct(id=pid, vector=vec, payload=payload))
        preview.append(
            {
                "id": pid,
                "chunk_index": i,
                "dimensions": dim,
                "vector_first_k": vec[:preview_dims],
                "text_preview": payload["text_preview"],
            }
        )

    client.upsert(collection_name=collection_name, points=points)

    return IngestResult(
        collection_name=collection_name,
        points_upserted=len(points),
        vector_dim=dim,
        model_name=model_name,
        points_preview=preview,
    )


def scroll_points_with_vectors(
    client: QdrantClient,
    collection_name: str,
    limit: int = 20,
    *,
    with_vectors: bool = True,
) -> list[dict[str, Any]]:
    """Fetch points from Qdrant including raw vectors (for teaching)."""
    records, _next = client.scroll(
        collection_name=collection_name,
        limit=limit,
        with_payload=True,
        with_vectors=with_vectors,
    )
    out: list[dict[str, Any]] = []
    for r in records:
        vec = r.vector
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


def summarize_vector(vec: list[float] | None, head: int = 16) -> dict[str, Any]:
    if not vec:
        return {"head": [], "l2_norm": None}
    h = min(head, len(vec))
    l2 = math.sqrt(sum(x * x for x in vec))
    return {"head": vec[:h], "l2_norm": l2, "length": len(vec)}


def main() -> None:
    import argparse
    import os

    from vector_db_env import load_vector_db_env

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

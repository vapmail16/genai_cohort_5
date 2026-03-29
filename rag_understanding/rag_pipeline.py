"""
rag_pipeline.py — End-to-end RAG pipeline
==========================================
What students learn:
  - The exact flow of a RAG system: Query → Embed → Retrieve → Generate
  - What "retrieval" looks like in code: a cosine similarity search in Qdrant
  - How the context (retrieved chunks) is formatted before being sent to the LLM
  - Prompt strategies: "stuff" (all at once) vs "refine" (iterative improvement)
  - The difference between a RAG answer and a raw LLM answer (no retrieval)
  - Basic evaluation concepts: did the answer use the retrieved context?

Pipeline:
  user query (str)
    └─ embed_query()           → 384-dim query vector
         └─ retrieve_chunks()  → top-K RetrievedChunk objects from Qdrant
              └─ format_context() → numbered context string
                   └─ generate_answer() → GenerationResult (answer + token counts)
                        └─ run_rag()    → RAGResult (everything bundled together)

  run_no_rag() → call the LLM with NO context (for side-by-side comparison)
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm


# ── Data classes returned by each pipeline stage ────────────────────────────

@dataclass
class RetrievedChunk:
    """One piece of text retrieved from Qdrant, with its relevance score."""
    id: str
    text: str
    score: float          # cosine similarity — higher is more relevant
    chunk_index: int
    source_file: str


@dataclass
class RAGResult:
    """Everything the pipeline produced for one user query."""
    query: str
    chunks: list[RetrievedChunk]
    context: str
    answer: str
    strategy: str                # "stuff" | "refine"
    retrieval_empty: bool        # True when no chunks passed the threshold
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = "gpt-4o-mini"


# ── Step 1: Embed the user's query ───────────────────────────────────────────

def embed_query(query: str, model_name: str | None = None) -> list[float]:
    """
    Turn the user's question into a 384-dim vector.
    We use the SAME embedding model as the ingestion pipeline so that
    query vectors and document vectors live in the same space.

    Teaching note: if you embed with model A but retrieve with model B,
    your similarity scores will be meaningless — they'd be in different spaces.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    model, _ = _load_encoder(model_name)
    import numpy as np
    vec = model.encode([query.strip()], convert_to_numpy=True, show_progress_bar=False)
    return vec[0].tolist()


def _load_encoder(model_name: str | None = None):
    """Lazy-load Sentence-Transformers (same model used for ingestion)."""
    from sentence_transformers import SentenceTransformer
    name = model_name or "sentence-transformers/all-MiniLM-L6-v2"
    return SentenceTransformer(name), name


# ── Step 2: Retrieve the most relevant chunks from Qdrant ───────────────────

def retrieve_chunks(
    client: QdrantClient,
    collection: str,
    query_vector: list[float],
    top_k: int = 5,
    score_threshold: float = 0.0,
) -> list[RetrievedChunk]:
    """
    Vector similarity search in Qdrant.

    Qdrant returns hits sorted by cosine similarity (highest first).
    `score_threshold` lets us filter out low-relevance chunks so the LLM
    doesn't get confused by barely-related content.

    Teaching note: this is the "retrieval" in RAG. The quality of this step
    directly determines the quality of the generated answer.
    """
    # qdrant-client >= 1.7 replaced .search() with .query_points()
    response = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )
    chunks: list[RetrievedChunk] = []
    for h in response.points:
        if h.score < score_threshold:
            continue
        payload = h.payload or {}
        chunks.append(RetrievedChunk(
            id=str(h.id),
            text=payload.get("text_preview", ""),
            score=h.score,
            chunk_index=payload.get("chunk_index", 0),
            source_file=payload.get("source_file", payload.get("source", "unknown")),
        ))
    return chunks


# ── Step 3: Format retrieved chunks into a numbered context string ───────────

def format_context(chunks: list[RetrievedChunk]) -> str:
    """
    Combine retrieved chunks into a readable context block for the LLM.
    Numbered references [1], [2] … match the citations we show in the UI.

    Teaching note: how you format context matters. Too much and the LLM gets
    distracted; too little and it doesn't have enough information to answer.
    """
    if not chunks:
        return ""
    parts: list[str] = []
    for i, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[{i}] (score: {chunk.score:.3f}, source: {chunk.source_file})\n{chunk.text}"
        )
    return "\n\n---\n\n".join(parts)


# ── Step 4a: Generate with "stuff" strategy — all context at once ────────────

_STUFF_SYSTEM = """You are a helpful assistant. Answer the user's question using ONLY the provided context.
If the context does not contain the answer, say "I don't have enough information in the retrieved documents to answer this."
Always end your answer with a "Sources:" line listing the [N] reference numbers you used."""

_STUFF_HUMAN = """Context:
{context}

Question: {query}

Answer:"""


# ── Step 4b: Generate with "refine" strategy — iterative improvement ─────────

_REFINE_INITIAL = """You are a helpful assistant. Answer the following question using the context below.
Context: {context}
Question: {query}
Initial answer:"""

_REFINE_UPDATE = """We have an existing answer: {existing_answer}

We have more context below:
{context}

Refine the existing answer using the new context. If the new context is not helpful, return the original answer unchanged.
Refined answer:"""


# ── Core generation helper (wraps OpenAI) ────────────────────────────────────

def openai_chat(messages: list[dict], model: str = "gpt-4o-mini", api_key: str | None = None):
    """
    Thin wrapper around the OpenAI Chat Completions API.
    Separated so tests can patch it without touching the OpenAI import.
    """
    from openai import OpenAI
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY is required for generation")
    client = OpenAI(api_key=key)
    return client.chat.completions.create(model=model, messages=messages)


def generate_answer(
    query: str,
    context: str,
    strategy: str = "stuff",
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> dict[str, Any]:
    """
    Call the LLM with the retrieved context and return the answer.

    Strategies:
      "stuff"  — feed ALL context to the LLM in one call. Simple, works well
                 for moderate amounts of context.
      "refine" — start with the first chunk, then iteratively refine the answer
                 with each subsequent chunk. Better for large contexts.

    Teaching note: the prompt is the "augmented" part of RAG. We're injecting
    retrieved knowledge directly into the prompt so the model can use it.
    """
    resolved_key = api_key or os.getenv("OPENAI_API_KEY", "")

    if strategy not in ("stuff", "refine"):
        raise ValueError(f"Unknown strategy {strategy!r}. Choose 'stuff' or 'refine'.")

    if not resolved_key:
        raise ValueError("OPENAI_API_KEY is required. Set it in rag_understanding/.env")

    if strategy == "stuff":
        messages = [
            {"role": "system", "content": _STUFF_SYSTEM},
            {"role": "user", "content": _STUFF_HUMAN.format(context=context, query=query)},
        ]
        resp = openai_chat(messages, model=model, api_key=resolved_key)
        return {
            "answer": resp.choices[0].message.content,
            "strategy": "stuff",
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
        }

    else:  # refine
        sections = context.split("\n\n---\n\n") if context else [""]
        messages = [{"role": "user", "content": _REFINE_INITIAL.format(
            context=sections[0], query=query)}]
        resp = openai_chat(messages, model=model, api_key=resolved_key)
        answer = resp.choices[0].message.content
        total_prompt = resp.usage.prompt_tokens
        total_completion = resp.usage.completion_tokens

        for section in sections[1:]:
            messages = [{"role": "user", "content": _REFINE_UPDATE.format(
                existing_answer=answer, context=section)}]
            resp = openai_chat(messages, model=model, api_key=resolved_key)
            answer = resp.choices[0].message.content
            total_prompt += resp.usage.prompt_tokens
            total_completion += resp.usage.completion_tokens

        return {
            "answer": answer,
            "strategy": "refine",
            "prompt_tokens": total_prompt,
            "completion_tokens": total_completion,
        }


# ── Comparison: LLM answer WITHOUT any retrieval ─────────────────────────────

def run_no_rag(
    query: str,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> str:
    """
    Ask the LLM the same question but with NO retrieved context.
    Used in the "RAG vs No-RAG" comparison to show hallucination risk
    and why grounding answers in retrieved documents matters.
    """
    resolved_key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not resolved_key:
        raise ValueError("OPENAI_API_KEY is required. Set it in rag_understanding/.env")

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the question to the best of your ability."},
        {"role": "user", "content": query},
    ]
    resp = openai_chat(messages, model=model, api_key=resolved_key)
    return resp.choices[0].message.content


# ── Full pipeline: query → embed → retrieve → generate → RAGResult ───────────

def run_rag(
    query: str,
    *,
    qdrant_url: str,
    api_key: str | None,
    openai_api_key: str | None,
    collection: str = "cohort_pdf_demo",
    top_k: int = 5,
    score_threshold: float = 0.0,
    strategy: str = "stuff",
    model: str = "gpt-4o-mini",
    embed_model: str | None = None,
) -> RAGResult:
    """
    Orchestrates the complete RAG pipeline for one user query.

    Teaching note: trace through this function step by step —
    each function call corresponds to a box in the RAG architecture diagram.
    """
    # Step 1 — embed the question
    query_vector = embed_query(query, model_name=embed_model)

    # Step 2 — retrieve relevant chunks from Qdrant
    client = QdrantClient(url=qdrant_url, api_key=api_key)
    chunks = retrieve_chunks(client, collection, query_vector, top_k=top_k,
                             score_threshold=score_threshold)

    retrieval_empty = len(chunks) == 0

    # Step 3 — format context (empty string if nothing retrieved)
    context = format_context(chunks)

    # Step 4 — generate: if no context, tell the LLM explicitly
    if retrieval_empty:
        gen_context = "No relevant documents were found in the knowledge base."
    else:
        gen_context = context

    gen = generate_answer(
        query=query,
        context=gen_context,
        strategy=strategy,
        model=model,
        api_key=openai_api_key,
    )

    return RAGResult(
        query=query,
        chunks=chunks,
        context=context,
        answer=gen["answer"],
        strategy=gen["strategy"],
        retrieval_empty=retrieval_empty,
        prompt_tokens=gen["prompt_tokens"],
        completion_tokens=gen["completion_tokens"],
        model=model,
    )

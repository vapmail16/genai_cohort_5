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


# ═══════════════════════════════════════════════════════════════════════════════
# RETRIEVAL IMPROVEMENT TECHNIQUES
# ═══════════════════════════════════════════════════════════════════════════════
# These functions answer the question: "score < 0.8 — how do we improve that?"
# Three independent, composable techniques are provided so the demo tab can
# show each one separately and then stack them.
# ═══════════════════════════════════════════════════════════════════════════════


# ── Technique 1: Query Expansion ─────────────────────────────────────────────

_EXPAND_PROMPT = """You are a search query optimizer.
Given a user's search query, rewrite it as a richer, more descriptive version
by adding relevant synonyms, related concepts, and alternative phrasings.
Keep it as a single sentence or short phrase (no longer than 30 words).
Return ONLY the expanded query — no explanation.

Original query: {query}
Expanded query:"""


def expand_query(query: str, api_key: str | None = None) -> str:
    """
    Technique 1 — Query Expansion.

    Why scores can be low: a short, vague query ("GDPR") embeds into a vector
    that may not land close to the chunks that contain the actual answer
    ("General Data Protection Regulation requires explicit consent…").

    Fix: ask the LLM to rewrite the query with synonyms and related terms,
    then embed the richer text. The new vector sits closer to the relevant
    chunks in the embedding space → higher cosine similarity scores.

    Teaching note: this is also called "HyDE-lite" or "query reformulation".
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    resolved_key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not resolved_key:
        raise ValueError("OPENAI_API_KEY is required for query expansion")

    messages = [{"role": "user", "content": _EXPAND_PROMPT.format(query=query.strip())}]
    resp = openai_chat(messages, model="gpt-4o-mini", api_key=resolved_key)
    expanded = resp.choices[0].message.content.strip()
    # Fallback: if the model returns nothing useful, keep original
    return expanded if expanded else query


# ── Technique 2: HNSW ef Tuning ──────────────────────────────────────────────

def retrieve_with_ef(
    client: QdrantClient,
    collection: str,
    query_vector: list[float],
    top_k: int = 5,
    ef: int = 128,
    score_threshold: float = 0.0,
) -> list[RetrievedChunk]:
    """
    Technique 2 — HNSW ef (exploration factor) tuning.

    Why scores can be low: Qdrant's HNSW index uses a default ef_search value
    that trades accuracy for speed. A low ef means the graph search terminates
    early and may miss some relevant vectors.

    Fix: raise ef_search. Higher ef → the HNSW graph explores more candidate
    nodes before picking the top-K → better recall → higher scores on the
    truly relevant chunks.

    Trade-off: higher ef = slightly more latency (still sub-100ms in practice).
    Typical sweet spot: ef=64 (fast), ef=128 (balanced), ef=256 (high recall).

    Teaching note: this is a zero-cost improvement — no re-ingestion needed,
    just a different search parameter at query time.
    """
    from qdrant_client.http import models as qm

    response = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        search_params=qm.SearchParams(hnsw_ef=ef),
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


# ── Technique 3: Re-ranking ───────────────────────────────────────────────────

def rerank_chunks(query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    """
    Technique 3 — Cross-encoder re-ranking.

    Why scores can be low (or misleading): bi-encoder cosine similarity is a
    coarse "first-pass" filter. It compares query and document independently,
    so nuance is lost. A chunk about "data retention rules" may score low
    against "GDPR" even though it's exactly what the user needs.

    Fix: run a cross-encoder over the (query, chunk) pairs. A cross-encoder
    reads BOTH texts together and produces a much more accurate relevance
    score. We then re-sort the chunks by the new score.

    Teaching note: the standard production pattern is
      bi-encoder (fast, top-100) → cross-encoder (slow but accurate, top-5).
    We use a lightweight model (ms-marco-MiniLM-L-6-v2) so it runs on CPU
    without a GPU and completes in < 1 second for 10 chunks.
    """
    if not chunks:
        return []

    # Lazy import — avoid loading the model at startup
    from sentence_transformers import CrossEncoder
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    pairs = [(query, c.text) for c in chunks]
    scores = model.predict(pairs)  # returns a numpy array

    # Build new RetrievedChunk objects with re-ranked scores, sorted descending
    reranked = []
    for chunk, new_score in zip(chunks, scores):
        # CrossEncoder scores are logits — convert to 0-1 range with sigmoid
        import math
        sig = 1.0 / (1.0 + math.exp(-float(new_score)))
        reranked.append(RetrievedChunk(
            id=chunk.id,
            text=chunk.text,
            score=round(sig, 4),
            chunk_index=chunk.chunk_index,
            source_file=chunk.source_file,
        ))

    return sorted(reranked, key=lambda c: c.score, reverse=True)


# ── Helper: Score threshold comparison ───────────────────────────────────────

def score_threshold_comparison(
    chunks: list[RetrievedChunk],
    thresholds: list[float],
) -> dict[float, list[RetrievedChunk]]:
    """
    Given a list of retrieved chunks, return a dict mapping each threshold to
    the subset of chunks that pass it.

    Used in the demo to show: "at 0.5 you get 8 chunks; at 0.8 only 2 pass —
    here's how to get more *good* chunks rather than lowering the bar."

    Teaching note: lowering the threshold is NOT the solution. Better retrieval
    techniques (expansion, ef tuning, reranking) raise the scores so that
    more chunks genuinely deserve to pass a high threshold.
    """
    return {t: [c for c in chunks if c.score >= t] for t in thresholds}


# ═══════════════════════════════════════════════════════════════════════════════
# HYDE — HYPOTHETICAL DOCUMENT EMBEDDINGS
# ═══════════════════════════════════════════════════════════════════════════════

_HYDE_PROMPT = """You are a search document generator.
Write a short paragraph (3–5 sentences) that would directly and completely answer
the following question. Write it as if it were an excerpt from a reference document.
Return ONLY the paragraph — no preamble, no explanation.

Question: {query}
Paragraph:"""


def embed_query_hyde(
    query: str,
    openai_key: str | None = None,
    model: str = "gpt-4o-mini",
    embed_model: str | None = None,
) -> tuple[list[float], str]:
    """
    HyDE — Hypothetical Document Embeddings (Gao et al., 2022).

    Instead of embedding the user's *question*, we ask the LLM to write a
    *hypothetical answer* and embed that instead.

    Why this works:
      Questions and answers live in different regions of embedding space.
      A question like "What is GDPR?" does not look like the chunks that
      answer it ("GDPR is the General Data Protection Regulation, enacted...").
      But a *hypothetical answer* lives right next to real answer chunks —
      they use the same vocabulary, structure, and concepts.

    Returns:
      (vector, hypothetical_text) — the vector to use for search,
      and the generated text (shown in the UI so students can inspect it).

    Teaching note: compare the HyDE vector search results to a normal
    embed_query() result on the same question — often the scores jump 0.1–0.2.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    resolved_key = openai_key or os.getenv("OPENAI_API_KEY", "")
    if not resolved_key:
        raise ValueError("OPENAI_API_KEY is required for HyDE")

    # Step 1 — generate the hypothetical document
    messages = [{"role": "user", "content": _HYDE_PROMPT.format(query=query.strip())}]
    resp = openai_chat(messages, model=model, api_key=resolved_key)
    hypothetical_text = resp.choices[0].message.content.strip()

    # Step 2 — embed the hypothetical document (not the original query)
    model_obj, _ = _load_encoder(embed_model)
    import numpy as np
    vec = model_obj.encode(
        [hypothetical_text], convert_to_numpy=True, show_progress_bar=False
    )
    return vec[0].tolist(), hypothetical_text


# ═══════════════════════════════════════════════════════════════════════════════
# RAGAS-STYLE EVALUATION
# ═══════════════════════════════════════════════════════════════════════════════
# We implement the 4 RAGAS metrics using direct LLM calls so students can see
# exactly what each metric is measuring — no black-box library required.
# ═══════════════════════════════════════════════════════════════════════════════

_FAITHFULNESS_PROMPT = """You are evaluating a RAG system's answer.

Context (retrieved documents):
{context}

Question: {query}
Answer: {answer}

Score the FAITHFULNESS of the answer:
- 1.0 = Every claim in the answer is directly supported by the context
- 0.5 = About half the claims are supported; the rest may be inferred
- 0.0 = The answer is entirely hallucinated — nothing is grounded in the context

Return ONLY valid JSON (no markdown):
{{"score": <float 0.0-1.0>, "reason": "<one sentence explanation>"}}"""

_ANSWER_RELEVANCY_PROMPT = """You are evaluating a RAG system's answer.

Question: {query}
Answer: {answer}

Score ANSWER RELEVANCY:
- 1.0 = The answer directly and completely addresses the question
- 0.5 = The answer is partially relevant or misses key aspects
- 0.0 = The answer is off-topic or does not address the question

Return ONLY valid JSON (no markdown):
{{"score": <float 0.0-1.0>, "reason": "<one sentence explanation>"}}"""

_CONTEXT_PRECISION_PROMPT = """You are evaluating a RAG system's retrieved context.

Question: {query}
Retrieved context chunks:
{context}

Score CONTEXT PRECISION — what fraction of the retrieved chunks are actually useful for answering the question?
- 1.0 = All retrieved chunks are relevant and useful
- 0.5 = About half the chunks are useful; the rest are noise
- 0.0 = None of the retrieved chunks help answer the question

Return ONLY valid JSON (no markdown):
{{"score": <float 0.0-1.0>, "reason": "<one sentence explanation>"}}"""

_CONTEXT_RECALL_PROMPT = """You are evaluating a RAG system's retrieved context.

Question: {query}
Ground-truth answer: {ground_truth}
Retrieved context chunks:
{context}

Score CONTEXT RECALL — how much of the ground-truth answer is covered by the retrieved context?
- 1.0 = The retrieved context contains everything needed to construct the ground-truth answer
- 0.5 = The context covers about half of what is needed
- 0.0 = The context is missing the information needed to answer

Return ONLY valid JSON (no markdown):
{{"score": <float 0.0-1.0>, "reason": "<one sentence explanation>"}}"""


def _call_eval_metric(prompt: str, api_key: str, model: str = "gpt-4o-mini") -> tuple[float, str]:
    """Call LLM to score one metric. Returns (score, reason)."""
    import json
    try:
        messages = [{"role": "user", "content": prompt}]
        resp = openai_chat(messages, model=model, api_key=api_key)
        content = resp.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        parsed = json.loads(content)
        score = float(parsed.get("score", 0.0))
        reason = str(parsed.get("reason", ""))
        return max(0.0, min(1.0, score)), reason
    except Exception:
        return 0.0, "Could not parse LLM response"


def evaluate_rag_answer(
    query: str,
    answer: str,
    contexts: list[str],
    ground_truth: str | None = None,
    openai_api_key: str | None = None,
    model: str = "gpt-4o-mini",
) -> dict:
    """
    RAGAS-style evaluation — score a RAG answer on 4 dimensions.

    Metrics (matches official RAGAS definitions):
      faithfulness       — is every claim in the answer grounded in the context?
      answer_relevancy   — does the answer address the question that was asked?
      context_precision  — are the retrieved chunks actually useful?
      context_recall     — (requires ground_truth) did we retrieve enough to answer fully?

    Returns a dict:
      {
        "faithfulness":      float 0-1,
        "answer_relevancy":  float 0-1,
        "context_precision": float 0-1,
        "context_recall":    float 0-1 | None,
        "overall":           float (average of available scores),
        "reasons": {
          "faithfulness":      str,
          "answer_relevancy":  str,
          "context_precision": str,
          "context_recall":    str | None,
        }
      }

    Teaching note: run this after every run_rag() call to see a scorecard.
    If faithfulness < 0.7, the LLM is hallucinating.
    If context_precision < 0.5, your chunking or retrieval needs work.
    """
    resolved_key = openai_api_key or os.getenv("OPENAI_API_KEY", "")
    if not resolved_key:
        raise ValueError("OPENAI_API_KEY is required for evaluation")

    # Short-circuit for empty answer
    if not answer.strip():
        return {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_precision": 0.0,
            "context_recall": None,
            "overall": 0.0,
            "reasons": {
                "faithfulness": "Answer is empty",
                "answer_relevancy": "Answer is empty",
                "context_precision": "Cannot evaluate without an answer",
                "context_recall": None,
            },
        }

    context_str = "\n\n---\n\n".join(
        f"[{i+1}] {c}" for i, c in enumerate(contexts)
    )

    # Score all three core metrics
    f_score, f_reason = _call_eval_metric(
        _FAITHFULNESS_PROMPT.format(context=context_str, query=query, answer=answer),
        api_key=resolved_key, model=model,
    )
    r_score, r_reason = _call_eval_metric(
        _ANSWER_RELEVANCY_PROMPT.format(query=query, answer=answer),
        api_key=resolved_key, model=model,
    )
    p_score, p_reason = _call_eval_metric(
        _CONTEXT_PRECISION_PROMPT.format(query=query, context=context_str),
        api_key=resolved_key, model=model,
    )

    # Optional context recall (requires ground truth)
    recall_score: float | None = None
    recall_reason: str | None = None
    if ground_truth:
        recall_score, recall_reason = _call_eval_metric(
            _CONTEXT_RECALL_PROMPT.format(
                query=query, ground_truth=ground_truth, context=context_str
            ),
            api_key=resolved_key, model=model,
        )

    scores = [f_score, r_score, p_score]
    if recall_score is not None:
        scores.append(recall_score)
    overall = sum(scores) / len(scores)

    return {
        "faithfulness":      f_score,
        "answer_relevancy":  r_score,
        "context_precision": p_score,
        "context_recall":    recall_score,
        "overall":           round(overall, 4),
        "reasons": {
            "faithfulness":      f_reason,
            "answer_relevancy":  r_reason,
            "context_precision": p_reason,
            "context_recall":    recall_reason,
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# METADATA-FILTERED RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════════

def retrieve_with_filter(
    client: QdrantClient,
    collection: str,
    query_vector: list[float],
    top_k: int = 5,
    filter_by: dict | None = None,
    score_threshold: float = 0.0,
) -> list[RetrievedChunk]:
    """
    Retrieve chunks with optional metadata filtering.

    filter_by is a dict of payload field → value, e.g.:
      {"source_file": "gdpr_policy.pdf"}
      {"source_file": "manual.pdf", "chunk_index": 5}

    Teaching note: filtering narrows the search to a subset of the collection
    *before* the similarity search runs. This is how enterprise RAG systems
    implement document-level access control and source-specific queries.

    If filter_by is empty or None, behaves identically to retrieve_chunks().
    """
    from qdrant_client.http import models as qm

    # Build Qdrant filter from the dict
    qdrant_filter = None
    if filter_by:
        conditions = [
            qm.FieldCondition(key=k, match=qm.MatchValue(value=v))
            for k, v in filter_by.items()
        ]
        qdrant_filter = qm.Filter(must=conditions)

    response = client.query_points(
        collection_name=collection,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=qdrant_filter,
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


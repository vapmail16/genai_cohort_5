"""
qdrant_lab.py — Streamlit UI for the PDF → Qdrant ingestion demo
================================================================
What students learn:
  - How the full ingestion pipeline connects to a UI (no LLM, no RAG)
  - That embeddings are produced locally by Sentence-Transformers,
    not by calling an LLM API
  - What a Qdrant "collection" is and what a "point" looks like (id + vector + payload)
  - How to inspect the actual float values stored in a vector database

This file is a pure UI layer — all pipeline logic lives in qdrant_pdf_pipeline.py.
Connection settings (URL, API key, collection name) come from vector_db_env.py
which reads vector_db_understanding/.env.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from qdrant_client import QdrantClient

# ── Import pipeline functions from the sibling module ────────────────────────
from qdrant_pdf_pipeline import (
    delete_qdrant_collection,
    ingest_pdf_to_qdrant,
    scroll_points_with_vectors,
    summarize_vector,
)

# ── Import env helpers — URL / key / collection from .env ────────────────────
from vector_db_env import (
    get_qdrant_api_key,
    get_qdrant_collection,
    get_qdrant_url,
    load_vector_db_env,
    resolve_api_key,
)


def show_qdrant_pdf_lab() -> None:
    # ── Load .env on every page visit (idempotent — only reads file once) ─────
    load_vector_db_env()

    st.markdown("### 📦 Qdrant PDF ingestion lab")
    st.markdown(
        """
        **What this is (and is not)**  
        - **Is:** extract text from a PDF → chunk → **Sentence-Transformers** embeddings on your machine → **upsert** to Qdrant → **scroll** points and show **dimensions + vector components**.  
        - **Is not:** no LLM, no retrieval-augmented answering, no "ask questions about the PDF" — that would be a separate RAG flow.

        **Connection:** set **`QDRANT_URL`** and **`QDRANT_API_KEY`** in `vector_db_understanding/.env` (see `.env.example`). Values below default from `.env`; you can override in the UI for demos.
        """
    )

    # ── Read defaults from .env — these pre-fill the sidebar inputs ───────────
    env_url = get_qdrant_url()
    env_collection = get_qdrant_collection()
    has_env_url = bool(env_url)
    has_env_key = get_qdrant_api_key() is not None

    # Warn early if critical config is missing so students know what to fix
    if not has_env_url:
        st.warning(
            "Add **`QDRANT_URL`** to `vector_db_understanding/.env` (copy from `.env.example`) "
            "or paste your cluster URL below."
        )
    if not has_env_key:
        st.info(
            "Optional: set **`QDRANT_API_KEY`** in `.env` for Qdrant Cloud, or paste a key below when ingesting."
        )

    # ── Sidebar: connection settings + chunking parameters ───────────────────
    with st.sidebar:
        st.header("Qdrant connection")
        qdrant_url = st.text_input(
            "Qdrant URL (HTTPS REST)",
            value=env_url,
            placeholder="https://xxxx.cloud.qdrant.io:6333",
            help="From `.env`: QDRANT_URL",
        )
        api_key_input = st.text_input(
            "API key",
            type="password",                   # masked — not shown on screen
            placeholder="Uses QDRANT_API_KEY from .env when left empty",
            help="Qdrant Cloud API key; optional if set in .env",
        )
        collection_name = st.text_input(
            "Collection name",
            value=env_collection,
            help="From .env: QDRANT_COLLECTION",
        )
        # chunk_size controls how much text goes into each embedding
        chunk_size = st.number_input("Chunk size (chars)", min_value=50, value=400, step=50)
        # overlap keeps context across chunk boundaries
        overlap = st.number_input("Overlap (chars)", min_value=0, value=50, step=10)
        # how many float values to show in the UI (full vector is 384 values)
        preview_dims = st.number_input("Show first N dimensions", min_value=4, value=12, step=2)

    # ── Resolve final API key: UI input beats .env ───────────────────────────
    effective_key = resolve_api_key(api_key_input)

    # ── File uploader ─────────────────────────────────────────────────────────
    uploaded = st.file_uploader("PDF file", type=["pdf"])

    # ── Action buttons ────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        # Disabled until a file is uploaded — avoids confusing errors
        run_ingest = st.button("Ingest PDF into Qdrant", type="primary", disabled=uploaded is None)
    with col_b:
        load_vectors = st.button("Scroll & show vectors from collection")

    # ── Clear collection — guarded by a checkbox to prevent accidents ─────────
    with st.expander("Clear collection (reset for a fresh ingest)"):
        st.caption(
            "Deletes the **entire** collection named in the sidebar from your Qdrant cluster "
            "(all vectors and payloads). Your next ingest recreates the collection."
        )
        confirm_clear = st.checkbox("I understand this deletes the collection and all its points")
        clear_collection = st.button(
            "Delete this collection",
            disabled=not confirm_clear,    # button is greyed out until confirmed
            help="Requires the checkbox above",
        )

        if clear_collection and confirm_clear:
            if not (qdrant_url or "").strip():
                st.error("Set **QDRANT_URL** in `.env` or enter a URL above.")
            else:
                with st.spinner("Deleting collection…"):
                    try:
                        msg = delete_qdrant_collection(
                            qdrant_url=(qdrant_url or "").strip(),
                            api_key=effective_key,
                            collection_name=(collection_name or "").strip() or env_collection,
                        )
                    except Exception as e:
                        st.error(f"Clear failed: {e}")
                        st.stop()
                st.success(msg)

    # ── Ingest action ─────────────────────────────────────────────────────────
    if run_ingest and uploaded is not None:
        if not (qdrant_url or "").strip():
            st.error("Set **QDRANT_URL** in `.env` or enter a URL above.")
            st.stop()
        with st.spinner("Extracting text, embedding locally, upserting to Qdrant…"):
            try:
                result = ingest_pdf_to_qdrant(
                    uploaded.getvalue(),           # bytes from Streamlit uploader
                    qdrant_url=(qdrant_url or "").strip(),
                    api_key=effective_key,
                    collection_name=(collection_name or "").strip() or env_collection,
                    chunk_size=int(chunk_size),
                    overlap=int(overlap),
                    preview_dims=int(preview_dims),
                )
            except Exception as e:
                st.error(f"Ingest failed: {e}")
                st.stop()

        # Show summary banner then the per-chunk preview table
        st.success(
            f"Upserted **{result.points_upserted}** points into `{result.collection_name}` "
            f"— **{result.vector_dim}**-dimensional vectors (`{result.model_name}`)."
        )
        # DataFrame columns: id, chunk_index, dimensions, vector_first_k, text_preview
        df = pd.DataFrame(result.points_preview)
        st.dataframe(df, use_container_width=True)

    # ── Scroll action — fetch + display stored points with raw vectors ────────
    if load_vectors:
        if not (qdrant_url or "").strip():
            st.error("Set **QDRANT_URL** in `.env` or enter a URL above.")
            st.stop()
        try:
            # Open a fresh client to scroll (separate from any ingest above)
            client = QdrantClient(url=(qdrant_url or "").strip(), api_key=effective_key)
            rows = scroll_points_with_vectors(
                client, (collection_name or "").strip() or env_collection, limit=50
            )
        except Exception as e:
            st.error(f"Scroll failed: {e}")
            st.stop()

        if not rows:
            st.warning("No points found (empty collection or wrong name).")
        else:
            st.subheader("Raw vectors from Qdrant")
            enriched = []
            for r in rows:
                vec = r.get("vector") or []
                # summarize_vector returns head floats + l2_norm for display
                summ = summarize_vector(vec, head=int(preview_dims))
                enriched.append(
                    {
                        "id": r["id"],
                        "dimensions": r.get("dimensions"),   # e.g. 384
                        "l2_norm": summ["l2_norm"],           # ≈ 1.0 for normalized vectors
                        "vector_head": summ["head"],          # first N floats
                        "text_preview": (r.get("payload") or {}).get("text_preview", ""),
                    }
                )
            st.dataframe(pd.DataFrame(enriched), use_container_width=True)

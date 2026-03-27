"""Streamlit lab: PDF → Qdrant with visible vectors (cohort demo)."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from qdrant_client import QdrantClient

from qdrant_pdf_pipeline import (
    ingest_pdf_to_qdrant,
    scroll_points_with_vectors,
    summarize_vector,
)


def show_qdrant_pdf_lab() -> None:
    st.markdown("### 📦 Qdrant PDF ingestion lab")
    st.markdown(
        """
        **Live demo**: run Qdrant locally (`docker compose up -d` in this folder), then ingest a PDF.
        You will see **chunk previews**, **embedding dimension**, and the **first values** of each stored vector.
        """
    )

    with st.sidebar:
        st.header("Qdrant connection")
        qdrant_url = st.text_input("Qdrant URL (REST)", "http://localhost:6333")
        api_key = st.text_input("API key (optional)", type="password")
        collection_name = st.text_input("Collection name", "cohort_pdf_demo")
        chunk_size = st.number_input("Chunk size (chars)", min_value=50, value=400, step=50)
        overlap = st.number_input("Overlap (chars)", min_value=0, value=50, step=10)
        preview_dims = st.number_input("Show first N dimensions", min_value=4, value=12, step=2)

    uploaded = st.file_uploader("PDF file", type=["pdf"])

    col_a, col_b = st.columns(2)
    with col_a:
        run_ingest = st.button("Ingest PDF into Qdrant", type="primary", disabled=uploaded is None)
    with col_b:
        load_vectors = st.button("Scroll & show vectors from collection")

    if run_ingest and uploaded is not None:
        with st.spinner("Extracting text, embedding, upserting…"):
            try:
                result = ingest_pdf_to_qdrant(
                    uploaded.getvalue(),
                    qdrant_url=qdrant_url,
                    api_key=api_key or None,
                    collection_name=collection_name,
                    chunk_size=int(chunk_size),
                    overlap=int(overlap),
                    preview_dims=int(preview_dims),
                )
            except Exception as e:
                st.error(f"Ingest failed: {e}")
                st.stop()

        st.success(
            f"Upserted **{result.points_upserted}** points into `{result.collection_name}` "
            f"— **{result.vector_dim}**-dimensional vectors (`{result.model_name}`)."
        )
        df = pd.DataFrame(result.points_preview)
        st.dataframe(df, use_container_width=True)

    if load_vectors:
        try:
            client = QdrantClient(url=qdrant_url, api_key=api_key or None)
            rows = scroll_points_with_vectors(client, collection_name, limit=50)
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
                summ = summarize_vector(vec, head=int(preview_dims))
                enriched.append(
                    {
                        "id": r["id"],
                        "dimensions": r.get("dimensions"),
                        "l2_norm": summ["l2_norm"],
                        "vector_head": summ["head"],
                        "text_preview": (r.get("payload") or {}).get("text_preview", ""),
                    }
                )
            st.dataframe(pd.DataFrame(enriched), use_container_width=True)

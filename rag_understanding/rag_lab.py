"""
rag_lab.py — Live RAG demo Streamlit page
==========================================
What students learn (by doing, not just reading):
  - How to connect a real LLM to a real vector database
  - The complete RAG pipeline: question → embed → retrieve → generate → answer
  - RAG vs No-RAG: side-by-side comparison showing why grounding matters
  - How retrieved chunk scores, sources, and order affect the final answer
  - Two prompting strategies: "stuff" (all-at-once) vs "refine" (iterative)
  - How score threshold filters out low-relevance noise
  - Token usage: how many tokens each call consumes

Prerequisites:
  1. Ingest a PDF in the "📦 Qdrant PDF lab" tab first (or any other collection).
  2. Add OPENAI_API_KEY to rag_understanding/.env
  3. Qdrant URL + API key must match what was used during ingestion.
"""

from __future__ import annotations

import streamlit as st

# ── Lazy imports for heavy deps (kept out of top-level for fast Streamlit start)
def _pipeline():
    import rag_pipeline as rp
    return rp


# ── Page entry point ──────────────────────────────────────────────────────────

def show_rag_lab():
    """
    Main entry point called by streamlit_app.py.
    Broken into tabs so each RAG feature gets focused screen space.
    """
    from rag_env import (
        get_qdrant_url, get_qdrant_api_key, get_qdrant_collection, get_openai_api_key,
    )

    st.markdown("## 🤖 Live RAG Demo — End-to-End")
    st.markdown(
        """
        This page connects to the **real Qdrant Cloud collection** you ingested in the
        *Qdrant PDF lab* tab and runs a **live RAG pipeline** using OpenAI as the generator.

        > **Prerequisites**: a PDF must already be ingested (use the 📦 Qdrant PDF lab first),
        > and `OPENAI_API_KEY` must be set in `rag_understanding/.env`.
        """
    )

    # ── Sidebar / connection settings ─────────────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔌 RAG Connections")
        qdrant_url = st.text_input(
            "Qdrant URL",
            value=get_qdrant_url(),
            help="Same URL used in the PDF ingestion lab",
            key="rag_qdrant_url",
        )
        qdrant_key = st.text_input(
            "Qdrant API key",
            value=get_qdrant_api_key() or "",
            type="password",
            key="rag_qdrant_key",
        )
        collection = st.text_input(
            "Collection name",
            value=get_qdrant_collection(),
            key="rag_collection",
        )
        openai_key = st.text_input(
            "OpenAI API key",
            value=get_openai_api_key() or "",
            type="password",
            key="rag_openai_key",
        )

        st.markdown("---")
        st.markdown("### ⚙️ Retrieval settings")
        top_k = st.slider("Top-K chunks", min_value=1, max_value=10, value=4,
                          help="How many chunks to retrieve from Qdrant")
        score_threshold = st.slider("Score threshold", 0.0, 1.0, 0.2, 0.05,
                                    help="Filter out chunks below this cosine similarity")
        strategy = st.radio("Prompt strategy", ["stuff", "refine"],
                            help="stuff = all chunks in one call; refine = iterative")
        model = st.selectbox("LLM model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                             help="GPT-4o-mini is fast and cheap for demos")

    # ── Connectivity checks ────────────────────────────────────────────────────
    if not qdrant_url:
        st.warning("⚠️ Qdrant URL not set. Add `QDRANT_URL` to `rag_understanding/.env`")
    if not openai_key:
        st.warning("⚠️ OpenAI key not set. Add `OPENAI_API_KEY` to `rag_understanding/.env`")

    # ── Tabs — each tab is one RAG feature ────────────────────────────────────
    tabs = st.tabs([
        "💬 Ask a Question",
        "⚔️ RAG vs No-RAG",
        "🔍 Retrieval Inspector",
        "🔄 Strategy Comparison",
        "📊 Token Usage",
    ])

    with tabs[0]:
        _tab_ask(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, strategy, model)

    with tabs[1]:
        _tab_comparison(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, model)

    with tabs[2]:
        _tab_retrieval_inspector(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold)

    with tabs[3]:
        _tab_strategy_compare(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, model)

    with tabs[4]:
        _tab_token_usage()


# ── Tab 1 — Ask a Question ────────────────────────────────────────────────────

def _tab_ask(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, strategy, model):
    st.markdown("### 💬 Ask a question about your ingested documents")
    st.markdown(
        "Type any question — the pipeline will **embed your query**, "
        "**retrieve the most relevant chunks** from Qdrant, then **generate an answer** "
        "grounded in those chunks."
    )

    query = st.text_input(
        "Your question",
        placeholder="e.g. What are the key findings in the document?",
        key="ask_query",
    )

    if st.button("🚀 Ask (RAG)", key="ask_btn", type="primary"):
        if not query.strip():
            st.error("Please enter a question.")
            return
        _require_credentials(qdrant_url, openai_key)

        rp = _pipeline()
        with st.spinner("Embedding query → retrieving chunks → generating answer…"):
            try:
                result = rp.run_rag(
                    query=query,
                    qdrant_url=qdrant_url,
                    api_key=qdrant_key or None,
                    openai_api_key=openai_key,
                    collection=collection,
                    top_k=top_k,
                    score_threshold=score_threshold,
                    strategy=strategy,
                    model=model,
                )
            except Exception as exc:
                st.error(f"Pipeline error: {exc}")
                return

        # Store in session so Token Usage tab can show it
        st.session_state["last_rag_result"] = result

        # ── Answer ──
        if result.retrieval_empty:
            st.warning("⚠️ No chunks retrieved above the score threshold. "
                       "Answer is based on LLM knowledge only (not grounded).")

        st.markdown("#### ✅ Answer")
        st.markdown(result.answer)

        # ── Retrieved chunks ──
        with st.expander(f"📄 {len(result.chunks)} retrieved chunk(s) — click to inspect"):
            for i, c in enumerate(result.chunks, start=1):
                _render_chunk(i, c)


# ── Tab 2 — RAG vs No-RAG ─────────────────────────────────────────────────────

def _tab_comparison(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, model):
    st.markdown("### ⚔️ RAG vs No-RAG — Side-by-Side")
    st.markdown(
        """
        Both calls go to the **same LLM** with the **same question**.
        - **RAG answer**: LLM sees the retrieved chunks from your documents.
        - **No-RAG answer**: LLM answers from memory only (hallucination risk).

        This is the most powerful demo to show *why* RAG exists.
        """
    )

    query = st.text_input(
        "Question to compare",
        placeholder="Ask something specific about your ingested documents",
        key="compare_query",
    )

    if st.button("⚔️ Compare RAG vs No-RAG", key="compare_btn", type="primary"):
        if not query.strip():
            st.error("Please enter a question.")
            return
        _require_credentials(qdrant_url, openai_key)

        rp = _pipeline()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🤖 RAG answer (grounded)")
            with st.spinner("Running RAG pipeline…"):
                try:
                    rag_result = rp.run_rag(
                        query=query,
                        qdrant_url=qdrant_url,
                        api_key=qdrant_key or None,
                        openai_api_key=openai_key,
                        collection=collection,
                        top_k=top_k,
                        score_threshold=score_threshold,
                        model=model,
                    )
                    st.success(rag_result.answer)
                    st.caption(
                        f"Based on {len(rag_result.chunks)} retrieved chunk(s) · "
                        f"{rag_result.prompt_tokens + rag_result.completion_tokens} tokens"
                    )
                    with st.expander("View retrieved chunks"):
                        for i, c in enumerate(rag_result.chunks, start=1):
                            _render_chunk(i, c)
                except Exception as exc:
                    st.error(f"RAG error: {exc}")

        with col2:
            st.markdown("#### 💭 No-RAG answer (from memory)")
            with st.spinner("Asking LLM without retrieval…"):
                try:
                    no_rag = rp.run_no_rag(query=query, model=model, api_key=openai_key)
                    st.info(no_rag)
                    st.caption("Based on LLM training data only — no document context")
                except Exception as exc:
                    st.error(f"No-RAG error: {exc}")

        st.markdown(
            """
            ---
            **What to notice:**
            - Does the RAG answer cite specific facts from your document?
            - Does the No-RAG answer confabulate (make up plausible-sounding details)?
            - Did the RAG answer say "I don't have enough information" when it should?
            """
        )


# ── Tab 3 — Retrieval Inspector ───────────────────────────────────────────────

def _tab_retrieval_inspector(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold):
    st.markdown("### 🔍 Retrieval Inspector — See What Gets Retrieved")
    st.markdown(
        """
        Retrieve chunks **without** generating an answer.
        Use this to understand and tune retrieval quality:
        - Are high-scoring chunks genuinely relevant?
        - Is the score threshold filtering out useful content?
        - Do different phrasings of the same question retrieve different chunks?
        """
    )

    query = st.text_input(
        "Query to inspect",
        placeholder="Phrase your question in different ways and compare",
        key="inspect_query",
    )

    if st.button("🔍 Retrieve chunks only", key="inspect_btn"):
        if not query.strip():
            st.error("Please enter a query.")
            return
        _require_credentials(qdrant_url, None)  # OpenAI not needed here

        rp = _pipeline()
        with st.spinner("Embedding and retrieving…"):
            try:
                query_vec = rp.embed_query(query)
                from qdrant_client import QdrantClient
                client = QdrantClient(url=qdrant_url, api_key=qdrant_key or None)
                chunks = rp.retrieve_chunks(
                    client, collection, query_vec,
                    top_k=top_k, score_threshold=score_threshold,
                )
            except Exception as exc:
                st.error(f"Retrieval error: {exc}")
                return

        if not chunks:
            st.warning("No chunks retrieved above the score threshold. "
                       "Try lowering the threshold or rephrasing the query.")
            return

        st.success(f"Retrieved {len(chunks)} chunk(s)")

        # ── Score bar chart ──
        import pandas as pd
        import plotly.express as px
        df = pd.DataFrame({
            "chunk": [f"[{i+1}] …{c.text[:40]}…" for i, c in enumerate(chunks)],
            "score": [c.score for c in chunks],
            "source": [c.source_file for c in chunks],
        })
        fig = px.bar(df, x="score", y="chunk", orientation="h", color="score",
                     color_continuous_scale="Blues", range_x=[0, 1],
                     title="Cosine similarity score per retrieved chunk")
        fig.update_layout(height=300 + len(chunks) * 40, yaxis={"autorange": "reversed"})
        st.plotly_chart(fig, use_container_width=True)

        # ── Full chunk text ──
        for i, c in enumerate(chunks, start=1):
            _render_chunk(i, c)

        # ── Context as LLM would see it ──
        with st.expander("📋 Context string sent to LLM (stuff strategy)"):
            ctx = rp.format_context(chunks)
            st.code(ctx, language="text")


# ── Tab 4 — Strategy Comparison ──────────────────────────────────────────────

def _tab_strategy_compare(qdrant_url, qdrant_key, collection, openai_key, top_k, score_threshold, model):
    st.markdown("### 🔄 Prompt Strategy Comparison")
    st.markdown(
        """
        **Stuff** — all retrieved chunks are placed in one big prompt.
        Simple and usually best for small-to-medium contexts.

        **Refine** — the LLM first answers using chunk 1, then iteratively
        improves the answer with each additional chunk. Better for large documents
        where a single prompt would exceed context length.

        Run the same question with both strategies and compare:
        """
    )

    query = st.text_input(
        "Question for strategy comparison",
        placeholder="Ask something that requires synthesising multiple parts of the document",
        key="strategy_query",
    )

    if st.button("🔄 Run both strategies", key="strategy_btn", type="primary"):
        if not query.strip():
            st.error("Please enter a question.")
            return
        _require_credentials(qdrant_url, openai_key)

        rp = _pipeline()

        col1, col2 = st.columns(2)

        for col, strat in [(col1, "stuff"), (col2, "refine")]:
            with col:
                st.markdown(f"#### {'📦' if strat == 'stuff' else '🔁'} {strat.capitalize()} strategy")
                with st.spinner(f"Running {strat}…"):
                    try:
                        result = rp.run_rag(
                            query=query,
                            qdrant_url=qdrant_url,
                            api_key=qdrant_key or None,
                            openai_api_key=openai_key,
                            collection=collection,
                            top_k=top_k,
                            score_threshold=score_threshold,
                            strategy=strat,
                            model=model,
                        )
                        st.markdown(result.answer)
                        st.caption(
                            f"Prompt tokens: {result.prompt_tokens} | "
                            f"Completion: {result.completion_tokens} | "
                            f"Total: {result.prompt_tokens + result.completion_tokens}"
                        )
                    except Exception as exc:
                        st.error(f"{strat} error: {exc}")

        st.markdown(
            """
            ---
            **Teaching note:** the *refine* strategy typically uses more tokens
            (multiple LLM calls) but can produce more nuanced answers when the
            context is long and complex.
            """
        )


# ── Tab 5 — Token Usage ───────────────────────────────────────────────────────

def _tab_token_usage():
    st.markdown("### 📊 Token Usage")
    st.markdown(
        """
        Token usage helps students understand the **cost and efficiency** of RAG.

        Run questions from the other tabs — this panel accumulates the token usage
        for each run so you can compare strategies.
        """
    )

    result = st.session_state.get("last_rag_result")
    if result is None:
        st.info("No results yet. Run a query from the 'Ask a Question' tab first.")
        return

    import pandas as pd
    import plotly.graph_objects as go

    prompt_t = result.prompt_tokens
    compl_t = result.completion_tokens
    total_t = prompt_t + compl_t

    col1, col2, col3 = st.columns(3)
    col1.metric("Prompt tokens", prompt_t,
                help="Tokens in the prompt (system + context + question)")
    col2.metric("Completion tokens", compl_t,
                help="Tokens in the generated answer")
    col3.metric("Total tokens", total_t)

    # Donut chart
    fig = go.Figure(go.Pie(
        labels=["Prompt (context + question)", "Completion (answer)"],
        values=[prompt_t, compl_t],
        hole=0.5,
        marker_colors=["#667eea", "#764ba2"],
    ))
    fig.update_layout(title=f"Token split — {result.strategy} strategy, {result.model}",
                      height=350)
    st.plotly_chart(fig, use_container_width=True)

    # Rough cost estimate (gpt-4o-mini pricing as of 2024)
    input_cost = (prompt_t / 1_000_000) * 0.15
    output_cost = (compl_t / 1_000_000) * 0.60
    st.caption(
        f"💰 Estimated cost (gpt-4o-mini): "
        f"${input_cost:.6f} input + ${output_cost:.6f} output "
        f"= **${input_cost + output_cost:.6f}** per query"
    )

    st.markdown(
        """
        ---
        **Why this matters:**
        - Retrieval adds tokens (the context chunks) but dramatically reduces hallucination.
        - The "stuff" strategy uses one LLM call; "refine" uses N calls (N = number of chunks).
        - Choosing the right model and top-K directly controls cost.
        """
    )


# ── Shared helpers ────────────────────────────────────────────────────────────

def _render_chunk(i: int, chunk) -> None:
    """Render a single RetrievedChunk with score badge and full text."""
    score_pct = int(chunk.score * 100)
    color = "#28a745" if score_pct >= 70 else "#ffc107" if score_pct >= 40 else "#dc3545"
    st.markdown(
        f"**[{i}]** &nbsp; "
        f"<span style='background:{color};color:white;padding:2px 8px;border-radius:4px;"
        f"font-size:0.8em'>{score_pct}% match</span> &nbsp; "
        f"<span style='color:#888;font-size:0.85em'>📄 {chunk.source_file} · chunk #{chunk.chunk_index}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(f"> {chunk.text}")
    st.markdown("")


def _require_credentials(qdrant_url: str, openai_key: str | None) -> None:
    """Raise a visible Streamlit error and stop if credentials are missing."""
    if not qdrant_url:
        st.error("Qdrant URL is required. Set it in the sidebar or `rag_understanding/.env`.")
        st.stop()
    if openai_key is not None and not openai_key:
        st.error("OpenAI API key is required. Set it in the sidebar or `rag_understanding/.env`.")
        st.stop()

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
        "🔧 Improve Low Scores",
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

    with tabs[5]:
        _tab_improve_scores(qdrant_url, qdrant_key, collection, openai_key, top_k)


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


# ── Tab 6 — Improve Low Scores ────────────────────────────────────────────────

def _tab_improve_scores(qdrant_url, qdrant_key, collection, openai_key, top_k):
    """
    Demo: "score < 0.8 — how do we improve that?"

    Shows three independent, composable techniques:
      1. Query Expansion  — a richer query embeds closer to relevant chunks
      2. HNSW ef tuning   — higher ef explores more graph nodes → better recall
      3. Re-ranking       — cross-encoder rescores chunks for true relevance

    The page runs each technique one at a time and shows score charts so
    participants can see the improvement visually.
    """
    import pandas as pd
    import plotly.graph_objects as go

    st.markdown("## 🔧 Score < 0.8? Here's How to Improve It")
    st.markdown(
        """
        When retrieval scores come back below **0.8**, it doesn't mean the
        information isn't in the database — it often means the search isn't
        finding it efficiently. Three techniques fix this, in order of cost:

        | Technique | What it does | Extra cost |
        |---|---|---|
        | **1. Query Expansion** | Rewrites your query with synonyms & related terms | 1 cheap LLM call |
        | **2. HNSW ef tuning** | Tells Qdrant to explore more graph nodes | ~5–20 ms extra latency |
        | **3. Re-ranking** | Cross-encoder rescores every chunk against the query | ~200–500 ms locally |

        > **Demo flow:** enter a short/vague query, see the baseline scores, then
        > apply each technique and watch the scores rise.
        """
    )

    st.markdown("---")

    query = st.text_input(
        "Enter a short or vague query (something that gives low scores)",
        placeholder='e.g. "GDPR" or "data" or "rights"',
        key="improve_query",
    )

    ef_value = st.select_slider(
        "HNSW ef value (technique 2)",
        options=[32, 64, 128, 256, 512],
        value=128,
        help="Default in Qdrant is typically 128. Higher = better recall, slightly slower.",
        key="improve_ef",
    )

    run_rerank = st.checkbox(
        "Also run re-ranking (technique 3) — downloads cross-encoder model on first run (~80 MB)",
        value=False,
        key="improve_rerank",
    )

    if st.button("🔬 Run improvement demo", key="improve_btn", type="primary"):
        if not query.strip():
            st.error("Please enter a query.")
            return
        _require_credentials(qdrant_url, None)

        rp = _pipeline()

        # ── Step 0: baseline retrieval ─────────────────────────────────────
        st.markdown("### Step 1 — Baseline retrieval")
        with st.spinner("Embedding original query and retrieving…"):
            try:
                from qdrant_client import QdrantClient
                client = QdrantClient(url=qdrant_url, api_key=qdrant_key or None)
                baseline_vec = rp.embed_query(query)
                baseline_chunks = rp.retrieve_chunks(
                    client, collection, baseline_vec, top_k=top_k,
                )
            except Exception as exc:
                st.error(f"Retrieval error: {exc}")
                return

        if not baseline_chunks:
            st.warning("No chunks retrieved at all. Make sure a PDF has been ingested.")
            return

        _show_score_chart(baseline_chunks, "Baseline scores", "#ef553b")
        st.caption(
            f"Average score: **{sum(c.score for c in baseline_chunks)/len(baseline_chunks):.3f}** "
            f"· Chunks above 0.8: **{sum(1 for c in baseline_chunks if c.score >= 0.8)}**"
        )

        # ── Step 1: Score threshold breakdown ──────────────────────────────
        st.markdown("### Step 2 — What different thresholds give you")
        st.markdown(
            "This shows why just *lowering* the threshold is the wrong answer — "
            "you get more chunks but they're less relevant."
        )
        comparison = rp.score_threshold_comparison(baseline_chunks, [0.5, 0.6, 0.7, 0.8])
        thresh_df = pd.DataFrame({
            "Threshold": [f"≥ {t}" for t in [0.5, 0.6, 0.7, 0.8]],
            "Chunks passing": [len(comparison[t]) for t in [0.5, 0.6, 0.7, 0.8]],
        })
        st.dataframe(thresh_df, hide_index=True, use_container_width=False)
        st.markdown(
            "> **Lesson:** Lowering the threshold lets in noise. "
            "The techniques below raise the *actual scores* instead."
        )

        # ── Step 2: Query Expansion ────────────────────────────────────────
        st.markdown("### Technique 1 — Query Expansion")

        if not openai_key:
            st.info("OpenAI key not set — skipping query expansion (needs 1 LLM call).")
            expanded_chunks = baseline_chunks
            expanded_query = query
        else:
            with st.spinner("Asking LLM to expand the query…"):
                try:
                    expanded_query = rp.expand_query(query, api_key=openai_key)
                    expanded_vec = rp.embed_query(expanded_query)
                    expanded_chunks = rp.retrieve_chunks(
                        client, collection, expanded_vec, top_k=top_k,
                    )
                except Exception as exc:
                    st.error(f"Query expansion error: {exc}")
                    expanded_chunks = baseline_chunks
                    expanded_query = query

            st.markdown(f"**Original query:** `{query}`")
            st.markdown(f"**Expanded query:** `{expanded_query}`")
            _show_score_chart(expanded_chunks, "After query expansion", "#00cc96")
            _show_score_delta(baseline_chunks, expanded_chunks, label="query expansion")

        # ── Step 3: HNSW ef tuning ─────────────────────────────────────────
        st.markdown(f"### Technique 2 — HNSW ef = {ef_value}")
        with st.spinner(f"Retrieving with ef={ef_value}…"):
            try:
                ef_chunks = rp.retrieve_with_ef(
                    client, collection, baseline_vec,
                    top_k=top_k, ef=ef_value,
                )
            except Exception as exc:
                st.warning(f"ef tuning not supported by this Qdrant plan: {exc}")
                ef_chunks = baseline_chunks

        _show_score_chart(ef_chunks, f"After HNSW ef={ef_value}", "#636efa")
        _show_score_delta(baseline_chunks, ef_chunks, label=f"ef={ef_value}")
        st.markdown(
            f"> The HNSW index now explores **{ef_value}** candidate nodes instead of the default, "
            "giving it a better chance of finding highly relevant vectors."
        )

        # ── Step 4: Re-ranking (optional) ──────────────────────────────────
        if run_rerank:
            st.markdown("### Technique 3 — Cross-encoder Re-ranking")
            st.markdown(
                "The cross-encoder reads the query and each chunk **together** "
                "and produces a much more accurate relevance score. "
                "The order (and scores) will change."
            )
            with st.spinner("Loading cross-encoder model and re-ranking…"):
                try:
                    reranked_chunks = rp.rerank_chunks(query, baseline_chunks)
                except Exception as exc:
                    st.error(f"Re-ranking error: {exc}")
                    reranked_chunks = baseline_chunks

            _show_score_chart(reranked_chunks, "After re-ranking", "#ab63fa")
            _show_score_delta(baseline_chunks, reranked_chunks, label="re-ranking")

            with st.expander("Why did the order change?"):
                st.markdown(
                    """
                    **Bi-encoder (cosine similarity)** embeds the query and each
                    chunk *separately*, then measures the angle between the vectors.
                    It's fast but loses nuance.

                    **Cross-encoder** feeds the query and chunk *together* as a
                    single input — it can see exactly which words in the chunk
                    answer the query. Much more accurate, but ~10–50× slower.

                    **Production pattern:** bi-encoder retrieves the top-100,
                    cross-encoder re-ranks to top-5 before sending to the LLM.
                    """
                )

        # ── Summary ────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📋 Summary")
        st.success(
            "**Three techniques to improve low scores — no re-ingestion needed:**\n\n"
            "1. **Query Expansion** → embed a richer query → vectors land closer to relevant chunks\n"
            "2. **HNSW ef tuning** → explore more graph nodes → find vectors that the default search missed\n"
            "3. **Re-ranking** → cross-encoder reads query + chunk together → much more accurate scores\n\n"
            "Stack all three for maximum improvement."
        )


# ── Score chart helpers ───────────────────────────────────────────────────────

def _show_score_chart(chunks, title: str, color: str) -> None:
    """Horizontal bar chart of chunk scores."""
    import plotly.graph_objects as go

    labels = [f"[{i+1}] {c.text[:35]}…" for i, c in enumerate(chunks)]
    scores = [c.score for c in chunks]

    fig = go.Figure(go.Bar(
        x=scores, y=labels, orientation="h",
        marker_color=color,
        text=[f"{s:.3f}" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(range=[0, 1], title="Cosine similarity score"),
        yaxis=dict(autorange="reversed"),
        height=max(250, len(chunks) * 50 + 80),
        margin=dict(l=10, r=60, t=40, b=20),
    )
    # Reference line at 0.8
    fig.add_vline(x=0.8, line_dash="dash", line_color="red",
                  annotation_text="0.8 target", annotation_position="top right")
    st.plotly_chart(fig, use_container_width=True)


def _show_score_delta(before: list, after: list, label: str) -> None:
    """Show average score before vs after as a compact metric row."""
    avg_before = sum(c.score for c in before) / len(before) if before else 0
    avg_after = sum(c.score for c in after) / len(after) if after else 0
    above_before = sum(1 for c in before if c.score >= 0.8)
    above_after = sum(1 for c in after if c.score >= 0.8)

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg score before", f"{avg_before:.3f}")
    c2.metric(f"Avg score after {label}", f"{avg_after:.3f}",
              delta=f"{avg_after - avg_before:+.3f}")
    c3.metric("Chunks ≥ 0.8", f"{above_after}",
              delta=f"{above_after - above_before:+d} vs baseline")


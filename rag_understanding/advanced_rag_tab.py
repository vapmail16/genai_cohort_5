"""
advanced_rag_tab.py — Advanced RAG: Principles, Patterns & Enterprise Use
=========================================================================
Covers 8 topic areas for cohort session:
  1. Real-World RAG Pipeline — chunking strategies & evolution
  2. Latest Principles 2025–2026 — retrieval augmentation patterns
  3. Advanced RAG Features — fusion, hybrid search, context compression
  4. RAG Evolution & Industry Trends — year-by-year shift
  5. Enterprise RAG Patterns — security, scale, observability, cost
  6. RAGAS Evaluation — faithfulness, relevance, precision, recall
  7. Common Pitfalls — what breaks RAG in production
  8. Real-World Problem Statements — 4 industry scenarios (no answers shown)
"""

from __future__ import annotations

import streamlit as st


def show_advanced_rag() -> None:
    """Entry point called by streamlit_app.py."""
    st.markdown("## 🚀 Advanced RAG — Principles, Patterns & Enterprise Use")
    st.markdown(
        "This module takes you from *basic retrieve-and-append* to "
        "**production-grade RAG systems** used in real enterprise settings in 2025–2026."
    )

    tabs = st.tabs([
        "📦 Real-World Pipeline",
        "🔬 Latest Principles 2025–26",
        "⚡ Advanced Features",
        "📈 RAG Evolution",
        "🏢 Enterprise Patterns",
        "📊 RAGAS Evaluation",
        "⚠️ Common Pitfalls",
        "🎯 Real-World Problems",
    ])

    with tabs[0]:
        _section_pipeline()
    with tabs[1]:
        _section_latest_principles()
    with tabs[2]:
        _section_advanced_features()
    with tabs[3]:
        _section_evolution()
    with tabs[4]:
        _section_enterprise()
    with tabs[5]:
        _section_ragas()
    with tabs[6]:
        _section_pitfalls()
    with tabs[7]:
        _section_problem_statements()


# ── Section 1: Real-World RAG Pipeline ───────────────────────────────────────

def _section_pipeline() -> None:
    st.markdown("### 📦 Real-World RAG Pipeline — Hands-on")

    st.markdown(
        """
        A production RAG pipeline is not just "retrieve + append". Every decision you
        make about *how* you split, store, and retrieve documents directly controls
        the quality of the final answer.
        """
    )

    with st.expander("🔪 Chunking Strategies — Fixed-size vs Semantic", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                #### Fixed-size chunking
                Split every N tokens regardless of meaning.

                ```python
                from langchain.text_splitter import CharacterTextSplitter

                splitter = CharacterTextSplitter(
                    chunk_size=512,
                    chunk_overlap=100,   # ~20% overlap
                    separator="\\n"
                )
                chunks = splitter.split_text(document)
                ```

                **When it works:** Simple documents, uniform prose.

                **When it breaks:** Splits mid-sentence, mid-code-block,
                mid-table → the retrieved chunk makes no sense on its own.
                """
            )
        with col2:
            st.markdown(
                """
                #### Semantic chunking (LlamaIndex approach)
                Split at *meaning boundaries* — paragraph ends, section headers.

                ```python
                from llama_index.core.node_parser import (
                    SemanticSplitterNodeParser
                )
                from llama_index.embeddings.openai import OpenAIEmbedding

                splitter = SemanticSplitterNodeParser(
                    buffer_size=1,
                    breakpoint_percentile_threshold=95,
                    embed_model=OpenAIEmbedding()
                )
                nodes = splitter.get_nodes_from_documents(docs)
                ```

                **Advantage:** Each chunk is a complete thought.
                Retrieval scores are 15–25% higher for the same query.
                """
            )

    with st.expander("📐 Why 20% Overlap Matters"):
        st.markdown(
            """
            Imagine this sentence split across two chunks:

            > Chunk 1: *"…the patient must not take aspirin if they have a known allergy to NSAIDs or a history of**"*
            > Chunk 2: *"**gastric bleeding.** Always consult a physician before…"*

            Without overlap, **both chunks are useless** — neither contains the complete rule.

            With **20% overlap**, the boundary content appears in both chunks.
            Whichever chunk is retrieved will contain the full, actionable sentence.

            ```
            doc = "A B C D E F G H I J"
            chunk_size = 5, overlap = 1 (20%)

            Chunk 1: A B C D E
            Chunk 2:     D E F G H   ← D and E appear again = the bridge
            Chunk 3:         G H I J
            ```

            **Rule of thumb:** 10–20% overlap for most documents.
            Increase to 30% for legal or medical text where every word matters.
            """
        )

    with st.expander("📏 Chunk Size Impact on Retrieval Quality"):
        import pandas as pd
        df = pd.DataFrame({
            "Chunk size": ["128 tokens", "256 tokens", "512 tokens", "1024 tokens"],
            "Precision": ["High", "Good", "Medium", "Low"],
            "Recall": ["Low", "Medium", "Good", "High"],
            "Risk": ["Too granular — misses context", "Sweet spot for most cases",
                     "Good for long paragraphs", "Too big — dilutes the relevant sentence"],
            "Best for": ["FAQ, structured data", "General knowledge bases",
                         "Technical manuals", "Summarisation tasks"],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.info(
            "**Golden rule:** chunk size should be ≤ 1/4 of your model's context window "
            "so you can fit 4+ chunks in a single prompt without truncation."
        )

    with st.expander("🏷️ Metadata Attachment — The Hidden Superpower"):
        st.markdown(
            """
            Every chunk should carry metadata so the retriever (and the LLM) knows
            *where* the information came from.

            ```python
            chunk = {
                "text": "The interest rate cap is 2% per quarter...",
                "metadata": {
                    "source":       "FCA_Policy_2024_v3.pdf",
                    "section":      "Section 4.2 — Interest Rate Controls",
                    "date":         "2024-11-01",
                    "page":         12,
                    "doc_type":     "regulatory",
                    "last_updated": "2025-01-15",
                }
            }
            ```

            **Why it matters:**
            - **Filtering:** `WHERE doc_type = 'regulatory' AND date > '2024-01-01'`
              → search only the relevant subset → faster + more accurate
            - **Citations:** the LLM can say *"According to Section 4.2 of FCA Policy 2024…"*
            - **Freshness:** auto-retire chunks older than N days
            """
        )


# ── Section 2: Latest Principles 2025–2026 ───────────────────────────────────

def _section_latest_principles() -> None:
    st.markdown("### 🔬 Latest Principles & Findings (2025–2026)")

    st.markdown(
        """
        The RAG field moved fast in 2024–2025. Here are the patterns that are now
        considered **standard practice** in production systems.
        """
    )

    st.markdown("#### Retrieval Augmentation Patterns")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ##### 🔀 Multi-vector Retrieval
            Use **three signals together**:
            - **Dense** (semantic, e.g. all-MiniLM)
            - **Sparse** (keyword, BM25)
            - **Keyword exact match** (regex/Elasticsearch)

            Fuse the ranked lists with **Reciprocal Rank Fusion (RRF)**
            so no single signal dominates.

            *Why:* Dense misses exact jargon ("FCA PS24/1").
            Sparse misses paraphrases. Together they cover both.
            """
        )

    with col2:
        st.markdown(
            """
            ##### 🔍 Query Expansion
            Before embedding, rewrite the query:

            ```python
            # Original: "GDPR fines"
            # Expanded:
            "GDPR financial penalties, data
            protection fines, Article 83
            enforcement, ICO sanctions"
            ```

            The expanded vector lands closer to
            relevant chunks in embedding space.

            *Effect:* +10–20% recall on vague queries.
            """
        )

    with col3:
        st.markdown(
            """
            ##### 💡 HyDE
            *Hypothetical Document Embeddings*

            Instead of embedding the **question**,
            ask the LLM to write a **hypothetical answer**,
            then embed *that*.

            ```python
            hyde = llm("Write a paragraph
            that would answer: " + query)
            vector = embed(hyde)  # not the query!
            results = qdrant.search(vector)
            ```

            *Why it works:* the hypothetical answer
            lives in the same vector space as
            real answer chunks → higher scores.
            """
        )

    st.markdown("---")
    st.markdown("#### Ranking & Reranking — Two-Stage Retrieval")

    st.markdown(
        """
        ```
        Stage 1 — Bi-encoder (fast, broad):
          embed(query) → cosine search → top 50 candidates   [~10ms]

        Stage 2 — Cross-encoder (slow, precise):
          cross_encoder(query, chunk_i) for i in top 50
          → re-sort → take top 5                              [~300ms]

        Send only top 5 to the LLM
        ```

        **Why not just use the cross-encoder for everything?**
        A cross-encoder reads both texts together — it's 50–100× more accurate
        but also 50–100× slower. You'd need ~5 seconds per query.
        The two-stage pattern gives you *accuracy of a cross-encoder at
        near-speed of a bi-encoder*.
        """
    )

    with st.expander("📐 Reciprocal Rank Fusion (RRF) explained simply"):
        st.markdown(
            """
            You have three ranked lists (dense, sparse, keyword).
            How do you blend them fairly?

            **RRF formula:**
            ```
            RRF_score(doc) = Σ  1 / (k + rank_in_list_i)
                             i
            where k = 60  (smoothing constant)
            ```

            **Example:**
            ```
            Doc A: rank 1 in dense, rank 3 in sparse, rank 2 in keyword
            RRF = 1/(60+1) + 1/(60+3) + 1/(60+2) = 0.0490

            Doc B: rank 5 in dense, rank 1 in sparse, rank 10 in keyword
            RRF = 1/(60+5) + 1/(60+1) + 1/(60+10) = 0.0467
            ```

            Doc A wins — it consistently appeared near the top across all
            three signals, which is stronger evidence of relevance than
            being #1 in only one signal.
            """
        )

    # ── Plain-language deep-dives (appended) ──────────────────────────────────

    st.markdown("---")
    st.markdown("### 💬 Plain-Language Explainers — Each Pattern in Depth")

    with st.expander("🔀 Multi-vector Retrieval — Everyday Analogy & Worked Example", expanded=False):
        st.markdown(
            """
            #### Think of it like searching for a book in a library

            Imagine you walk into a library and ask: *"Do you have anything about data privacy fines?"*

            The librarian uses **three systems** at the same time:

            | System | How it works | What it's good at |
            |--------|-------------|-------------------|
            | 🧠 **Dense (semantic)** | Understands *meaning* — finds books about "data protection penalties" even if you said "fines" | Paraphrases, concepts |
            | 🔑 **Sparse (BM25/keyword)** | Finds exact words — "GDPR Article 83" | Product codes, proper names, jargon |
            | 📖 **Keyword exact match** | Regex/grep — finds the literal string | Reference numbers, IDs |

            **Why not just use one?**

            > You ask: *"What is the FCA PS24/1 rule?"*
            >
            > - Dense search returns: *"Financial Conduct Authority policies on consumer protection"* — close but wrong document
            > - Keyword search finds: the exact document titled **"FCA PS24/1"** immediately
            >
            > You ask: *"What are the rules about treating customers fairly?"*
            >
            > - Keyword search finds nothing — that phrase doesn't appear verbatim
            > - Dense search finds: **"TCF (Treating Customers Fairly) framework, Principle 6"** — exactly right

            **Together they never miss.** You fuse the results with RRF (see below) so the
            document that appears near the top of ALL three lists wins.

            #### Real-world impact
            Studies on domain-specific corpora (legal, medical, financial) show:
            - Dense-only: ~72% recall
            - Sparse-only: ~65% recall
            - Hybrid: **~89% recall** — consistently beats either alone
            """
        )

    with st.expander("🔍 Query Expansion — Worked Example Step by Step", expanded=False):
        st.markdown(
            """
            #### The problem: your query is too short

            When a user types *"GDPR fines"*, the embedding model converts that 2-word phrase
            into a vector. That vector sits in a specific spot in 384-dimensional space.

            The relevant chunks in your database might say:
            - *"Article 83(5) imposes administrative fines up to €20 million"*
            - *"The ICO issued a penalty notice for…"*
            - *"Maximum sanctions under the UK Data Protection Act…"*

            None of these contain the words "GDPR fines" — they use synonyms.
            The vector for *"GDPR fines"* may not be close enough to retrieve them.

            #### The fix: ask the LLM to be your search expert

            ```python
            EXPAND_PROMPT = \"\"\"
            You are a search query expert. Rewrite this query as a rich,
            descriptive sentence (max 30 words) using synonyms and related concepts.
            Only return the expanded query, nothing else.

            Query: {query}
            \"\"\"

            # Original query
            query = "GDPR fines"

            # Expanded (what the LLM returns)
            expanded = "GDPR data protection financial penalties Article 83 ICO enforcement \
sanctions European data privacy regulation fines maximum €20 million"

            # Now embed the EXPANDED query, not the original
            vector = embed(expanded)
            results = qdrant.search(vector)
            ```

            #### Before vs After

            | | Original query | Expanded query |
            |-|---------------|----------------|
            | Query sent to embed | `"GDPR fines"` | `"GDPR financial penalties Article 83 ICO enforcement…"` |
            | Top result score | 0.61 | 0.84 |
            | Relevant chunks in top-5 | 2/5 | 5/5 |

            #### When does it help most?
            - Short queries (1–3 words)
            - Technical jargon the user doesn't know how to phrase
            - Non-native speakers who use informal language
            - Voice search where queries are naturally short
            """
        )

    with st.expander("💡 HyDE — The Counterintuitive Trick That Works", expanded=False):
        st.markdown(
            """
            #### Normal RAG: embed the question, find similar documents

            ```
            User: "What is the maximum GDPR fine?"
                       ↓  embed
            Query vector: [0.12, -0.34, 0.88, ...]
                       ↓  cosine search
            Finds: chunks about "GDPR enforcement", "data protection rules"
            ```

            This works — but the question and the answer *look different* in embedding space.
            A question lives near other questions. The answer lives near other answers.

            #### HyDE: embed a hypothetical answer instead

            ```python
            # Step 1: Ask the LLM to imagine the answer
            hyde_prompt = f"Write a paragraph that would directly answer: {query}"
            hypothetical = llm(hyde_prompt)
            # Returns: "Under Article 83(5) of the GDPR, the maximum administrative
            #           fine is €20 million or 4% of total annual worldwide turnover,
            #           whichever is higher. The ICO in the UK applies equivalent..."

            # Step 2: Embed the HYPOTHETICAL ANSWER (not the question)
            vector = embed(hypothetical)

            # Step 3: Search — now you're matching answer-to-answer, not question-to-answer
            results = qdrant.search(vector)
            ```

            #### Why does this work?

            Think of it like matching resumes to a job.

            - Normal: you search using the *job title* ("Software Engineer")
            - HyDE: you first write an *ideal candidate description*, then match resumes to that

            The ideal description lives in the same space as real resumes.
            The job title doesn't.

            #### When to use HyDE vs Query Expansion

            | Situation | Better choice |
            |-----------|--------------|
            | Query is vague or short | Query Expansion |
            | Query is clear but documents use different vocabulary | HyDE |
            | Domain is highly technical (legal, medical) | HyDE |
            | You want to combine both | Run both, fuse with RRF |
            | Latency is critical (< 200ms) | Query Expansion (HyDE adds 1 LLM call) |
            """
        )

    with st.expander("🏆 Ranking & Reranking — Why Order Matters More Than You Think", expanded=False):
        st.markdown(
            """
            #### The "Lost in the Middle" problem

            Research (Liu et al., 2023) showed that GPT-4 performs significantly worse
            when the relevant information is in the **middle** of a long context.
            It pays most attention to the **beginning** and **end**.

            If you retrieve 10 chunks and the answer is in chunk 7 — the LLM may ignore it.

            **Reranking solves this** by putting the most relevant chunks first
            so the LLM sees them at the top.

            #### Bi-encoder vs Cross-encoder — the key difference

            ```
            Bi-encoder (what Qdrant/cosine does):
            ┌─────────────┐         ┌──────────────┐
            │    Query    │ → vec → │              │
            └─────────────┘         │  Score =     │
                                    │  cos(q, d)   │
            ┌─────────────┐         │              │
            │  Document   │ → vec → │              │
            └─────────────┘         └──────────────┘

            They're encoded SEPARATELY, then compared.
            Fast but loses nuance — can't see word interactions.

            Cross-encoder (reranker):
            ┌──────────────────────────────────┐
            │  [Query] [SEP] [Document]        │
            │                                  │
            │  Transformer reads BOTH together │
            │  → outputs relevance score 0–1   │
            └──────────────────────────────────┘

            Reads them TOGETHER — sees exactly which words in the
            document answer which words in the query. Much more accurate.
            ```

            #### Worked example

            Query: *"What side effects does aspirin have on the stomach?"*

            | Chunk | Bi-encoder score | Cross-encoder score | Why |
            |-------|-----------------|--------------------|----|
            | "Aspirin is an analgesic and antipyretic drug" | 0.78 | 0.21 | Mentions aspirin but not stomach |
            | "NSAIDs can cause gastric irritation and ulcers" | 0.71 | 0.88 | Directly answers — cross-encoder gets it |
            | "Aspirin reduces fever by blocking COX enzymes" | 0.69 | 0.19 | Mechanism, not side effects |
            | "Aspirin may cause gastric bleeding especially in elderly" | 0.65 | 0.94 | Best answer — bi-encoder ranked it 4th! |

            Without reranking: you'd send the wrong chunk first to the LLM.
            With reranking: the genuinely useful chunk goes first.

            #### The two-stage pattern in numbers

            ```
            Without reranking:  retrieve top-5, send all 5 to LLM
              → avg faithfulness: 0.71
              → cost: 2,500 tokens per query

            With reranking:     retrieve top-20, rerank, send top-3
              → avg faithfulness: 0.91   (+28%)
              → cost: 1,200 tokens per query  (52% cheaper)
            ```
            """
        )

    with st.expander("📐 RRF Deep Dive — Building Intuition with a Full Example", expanded=False):
        st.markdown(
            """
            #### Setup: you've run three searches for "GDPR fines UK"

            ```
            Dense search results:         Sparse (BM25) results:    Keyword results:
            1. Doc-C (GDPR UK fines)      1. Doc-B (exact phrase)   1. Doc-B
            2. Doc-A (EU data law)        2. Doc-C                  2. Doc-D
            3. Doc-D (ICO penalties)      3. Doc-A                  3. Doc-C
            4. Doc-B (ICO enforcement)    4. Doc-E                  4. Doc-A
            5. Doc-E (privacy rules)      5. Doc-D                  5. Doc-E
            ```

            #### Calculate RRF score for each document (k=60)

            | Doc | Dense rank | Sparse rank | Keyword rank | RRF score |
            |-----|-----------|------------|-------------|-----------|
            | **Doc-C** | 1 → 1/61 = 0.01639 | 2 → 1/62 = 0.01613 | 3 → 1/63 = 0.01587 | **0.04839** |
            | **Doc-B** | 4 → 1/64 = 0.01563 | 1 → 1/61 = 0.01639 | 1 → 1/61 = 0.01639 | **0.04841** |
            | **Doc-A** | 2 → 1/62 = 0.01613 | 3 → 1/63 = 0.01587 | 4 → 1/64 = 0.01563 | **0.04763** |
            | **Doc-D** | 3 → 1/63 = 0.01587 | 5 → 1/65 = 0.01538 | 2 → 1/62 = 0.01613 | **0.04738** |
            | **Doc-E** | 5 → 1/65 = 0.01538 | 4 → 1/64 = 0.01563 | 5 → 1/65 = 0.01538 | **0.04639** |

            #### Final ranking after RRF

            ```
            1. Doc-B  (0.04841) ← was rank 4 in dense! Dominated keyword + sparse
            2. Doc-C  (0.04839) ← was rank 1 in dense, consistent across all
            3. Doc-A  (0.04763)
            4. Doc-D  (0.04738)
            5. Doc-E  (0.04639)
            ```

            #### Key insight

            Doc-B was ranked **4th** by semantic search but was **#1 in two other signals**.
            RRF correctly promotes it because **consistent performance across multiple signals
            is stronger evidence than a single #1 ranking**.

            The constant k=60 is there to prevent a single rank-1 result from completely
            dominating. Without it: 1/1 = 1.0 vs 1/2 = 0.5 — first place wins too easily.
            With k=60: 1/61 = 0.0164 vs 1/62 = 0.0161 — only a tiny gap, consistency wins.
            """
        )


# ── Section 3: Advanced Features ─────────────────────────────────────────────

def _section_advanced_features() -> None:
    st.markdown("### ⚡ Advanced RAG Features")

    st.markdown("#### Fusion & Hybrid Search — BM25 + Vector")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            """
            **BM25 (keyword)** excels at:
            - Exact term matching: `"Article 83(4) GDPR"`
            - Product codes: `"SKU-X4492-B"`
            - Proper nouns: `"Pfizer Comirnaty"`
            - Short, precise queries

            **Vector search** excels at:
            - Paraphrases: *"data privacy rules"* → finds *"GDPR compliance requirements"*
            - Conceptual queries: *"side effects of blood thinners"*
            - Cross-language: query in English, docs in French

            **Combined (hybrid):** wins on *both* domains simultaneously.
            """
        )
    with col2:
        st.markdown(
            """
            ```python
            from qdrant_client.http import models as qm

            # Qdrant hybrid search
            results = client.query_points(
                collection_name="docs",
                prefetch=[
                    # Dense (semantic)
                    qm.Prefetch(
                        query=dense_vector,
                        using="dense",
                        limit=20
                    ),
                    # Sparse (BM25)
                    qm.Prefetch(
                        query=qm.SparseVector(
                            indices=bm25_indices,
                            values=bm25_values
                        ),
                        using="sparse",
                        limit=20
                    ),
                ],
                query=qm.FusionQuery(
                    fusion=qm.Fusion.RRF  # blend with RRF
                ),
                limit=5
            )
            ```
            """
        )

    st.markdown("---")
    st.markdown("#### Context Compression — LLMLingua")

    st.markdown(
        """
        **The problem:** you retrieve 5 chunks × 512 tokens = 2,560 tokens of context.
        But only ~300 tokens actually answer the question. The rest is noise that:
        - Wastes tokens (costs money)
        - Confuses the LLM ("lost in the middle" effect)
        - Slows down response time

        **LLMLingua** uses a small LM (e.g. LLaMA-7B) to score every token's
        relevance to the query, then drops the low-scoring ones:

        ```python
        from llmlingua import PromptCompressor

        compressor = PromptCompressor(model_name="NousResearch/Llama-2-7b-hf")

        compressed = compressor.compress_prompt(
            context_chunks,
            instruction=query,
            target_token=300,         # compress to 300 tokens
            rate=0.5,                 # drop ~50% of tokens
        )
        # Result: same meaning, half the tokens
        ```

        **Results (published benchmarks):**
        """
    )

    import pandas as pd
    df = pd.DataFrame({
        "Metric": ["Tokens sent to LLM", "Cost per query", "Latency", "Accuracy"],
        "Without compression": ["2,560", "$0.0077", "3.2s", "Baseline"],
        "With LLMLingua": ["820", "$0.0025", "1.8s", "+2.1% F1"],
        "Improvement": ["68% fewer", "67% cheaper", "44% faster", "Slightly better"],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.success(
        "**Key insight:** compressing context doesn't hurt accuracy — it often *improves* it "
        "because you remove the distracting noise that causes the LLM to wander."
    )

    # ── Plain-language deep-dives (appended) ──────────────────────────────────

    st.markdown("---")
    st.markdown("### 💬 Plain-Language Explainers — Advanced Features in Depth")

    with st.expander("🔀 Hybrid Search — Why It Beats Vector-Only on Real Queries", expanded=False):
        st.markdown(
            """
            #### The problem with pure vector search

            Vector search finds *semantically similar* content. But similarity ≠ relevance.

            > Query: *"What does regulation PS24/1 say about mortgage advice?"*
            >
            > Vector search returns: documents about "mortgage lending guidance", "consumer advice rules"
            > — these are *semantically similar* but **none of them is PS24/1**.
            >
            > BM25 (keyword) search returns: the exact document titled "PS24/1"
            > — because it matched the *exact string*.

            #### Real-world query types and which search wins

            | Query type | Example | Best signal |
            |-----------|---------|-------------|
            | Exact reference | "FCA PS24/1", "SKU-X4492" | BM25 |
            | Concept / paraphrase | "rules about treating customers fairly" | Dense vector |
            | Mixed | "FCA rules on customer fairness" | **Hybrid** |
            | Medical term | "Pfizer Comirnaty" | BM25 |
            | Symptom description | "chest tightness when climbing stairs" | Dense vector |

            #### How hybrid search works in practice

            ```
            User query: "GDPR penalties for data breach"

            ┌──────────────────┐    ┌──────────────────┐
            │  Dense search    │    │  BM25 search     │
            │  (semantic)      │    │  (keyword)       │
            │                  │    │                  │
            │  1. Doc-A (0.87) │    │  1. Doc-C (12.3) │
            │  2. Doc-C (0.82) │    │  2. Doc-A (10.1) │
            │  3. Doc-E (0.79) │    │  3. Doc-B (8.7)  │
            └──────────────────┘    └──────────────────┘
                        ↓                   ↓
                    ┌───────────────────────┐
                    │   RRF Fusion          │
                    │   Final ranking:      │
                    │   1. Doc-A  (both top)│
                    │   2. Doc-C  (both top)│
                    │   3. Doc-B            │
                    └───────────────────────┘
                              ↓
                    Send top-3 to LLM
            ```

            #### Why "sparse is free"

            BM25 doesn't need a GPU or an embedding model API call.
            It runs in milliseconds on a CPU using simple term frequency math.
            Adding it to your pipeline costs almost nothing but lifts recall significantly.

            **Bottom line:** if you're building a production RAG system in 2025,
            hybrid search is the default — not an optional extra.
            """
        )

    with st.expander("✂️ Context Compression — Simple Analogy & When to Use It", expanded=False):
        st.markdown(
            """
            #### The problem: you retrieved a newspaper but only needed one paragraph

            Imagine your RAG system retrieves 5 chunks about aspirin.
            Each chunk is 512 tokens. Total: 2,560 tokens sent to GPT-4.

            But the actual answer — "aspirin can cause gastric bleeding" —
            is **one sentence** buried in chunk 3. The other 2,540 tokens are noise.

            You're paying for 2,560 tokens but getting value from ~20.

            #### What LLMLingua actually does

            It uses a small language model to score every token:
            *"Given this query, how likely is this token to be important?"*

            ```
            Query: "What are aspirin's side effects on the stomach?"

            Original chunk (50 tokens):
            "Aspirin, discovered in 1897 by Felix Hoffmann at Bayer,
            is a widely used analgesic. It works by inhibiting COX enzymes.
            It can cause gastric irritation and bleeding, particularly
            in elderly patients or those with a history of ulcers."

            After LLMLingua compression (25 tokens, 50% reduction):
            "Aspirin ... cause gastric irritation bleeding particularly
            elderly patients history ulcers."

            The meaning is preserved. The fluff is gone.
            ```

            #### When to use compression

            | Situation | Use compression? |
            |-----------|-----------------|
            | 1–2 short chunks retrieved | ❌ Not worth the overhead |
            | 5+ chunks, context > 2,000 tokens | ✅ Yes |
            | Legal / medical (exact wording matters) | ⚠️ Be cautious — verify output |
            | Latency is critical (< 500ms) | ❌ Adds ~200ms |
            | Cost is critical (many queries/day) | ✅ Saves 60–70% LLM cost |

            #### The "lost in the middle" connection

            Compression also solves the attention problem.
            LLMs pay less attention to content in the middle of long prompts.

            A compressed prompt of 400 tokens means the LLM reads *everything*.
            A full prompt of 3,000 tokens means it may skim the middle.

            **Think of it like a meeting summary vs full transcript.**
            The summary forces you to engage with every point.
            The transcript buries the important bits.
            """
        )

def _section_evolution() -> None:
    st.markdown("### 📈 RAG Evolution & Industry Trends")

    import pandas as pd
    df = pd.DataFrame({
        "Year": ["2023", "2024", "2025", "2026"],
        "Shift": [
            "Basic RAG — retrieve + append",
            "Chunking + reranking focus",
            "Hybrid search + adaptive retrieval",
            "Multi-modal RAG + agent-driven retrieval",
        ],
        "Impact": [
            "Slow, expensive, high token waste",
            "30–40% accuracy lift",
            "Production-grade accuracy",
            "Images, tables, reasoning",
        ],
        "What changed": [
            "Proof of concept — just works",
            "Quality became measurable (RAGAS)",
            "Hybrid search became standard; LLMs used to verify retrieval",
            "Agents decide *when* and *what* to retrieve dynamically",
        ],
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown(
        """
        ---
        ### The Core Evolution

        ```
        2023  →  "Retrieve all, append all"
                  Query → embed → top-K → stuff into prompt → generate

        2024  →  "Retrieve smart"
                  Query → chunk better → retrieve → rerank → generate

        2025  →  "Retrieve smart, compress, verify"
                  Query → expand → hybrid retrieve → rerank → compress → verify → generate

        2026  →  "Agent decides"
                  Agent decomposes query → decides retrieval strategy per sub-question
                  → multi-modal → verifies → cites → adapts based on feedback
        ```
        """
    )

    with st.expander("🤔 Why did basic RAG fail in production?"):
        st.markdown(
            """
            **Problem 1 — Token waste:**
            Appending 10 chunks × 1000 tokens = 10K tokens per query.
            At GPT-4 pricing that's $0.30 per query. At 10,000 queries/day = $3,000/day.

            **Problem 2 — "Lost in the middle":**
            LLMs pay less attention to context in the middle of a long prompt.
            If the answer is in chunk 5 of 10, it may be ignored.

            **Problem 3 — Retrieval noise:**
            Top-10 cosine similarity includes 3–4 chunks that are technically similar
            but don't contain the answer. The LLM hallucinates to fill the gap.

            **Problem 4 — No verification:**
            Basic RAG has no step that checks: "did I retrieve something useful?"
            If the answer isn't in the KB, the LLM makes one up.

            **Modern RAG fixes all four** with reranking, compression, and verification steps.
            """
        )


# ── Section 5: Enterprise Patterns ───────────────────────────────────────────

def _section_enterprise() -> None:
    st.markdown("### 🏢 Enterprise RAG Patterns")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔒 Security & Access Control",
        "📡 Scalability",
        "🔍 Observability & Debugging",
        "💰 Cost Optimisation",
    ])

    with tab1:
        st.markdown(
            """
            #### Document-Level Permissions (Multi-tenant RAG)

            **The problem:** your vector DB contains docs from 50 different customers.
            Customer A must never see Customer B's data — even if their query
            semantically matches Customer B's documents.

            ```python
            # At ingestion time — tag every chunk with its tenant
            client.upsert(
                collection_name="enterprise_kb",
                points=[PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "text":      chunk_text,
                        "tenant_id": "customer_A",   # ← access control tag
                        "clearance": "confidential", # ← security level
                        "doc_id":    "policy_v3.pdf",
                    }
                )]
            )

            # At query time — filter BEFORE similarity search
            from qdrant_client.http.models import Filter, FieldCondition, MatchValue

            results = client.query_points(
                collection_name="enterprise_kb",
                query=query_vector,
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="tenant_id",
                            match=MatchValue(value=current_user.tenant_id)
                        )
                    ]
                ),
                limit=5
            )
            ```

            #### PII Redaction Before Retrieval

            Never store raw PII in the vector DB payload.
            Redact before ingestion, store a reference:

            ```python
            # Before ingestion
            text = "Patient John Smith (DOB 15/03/1982) was prescribed..."
            redacted = "Patient [REDACTED] (DOB [REDACTED]) was prescribed..."
            # Store redacted text; keep PII mapping in a separate secure store
            ```

            #### Audit Logging

            Every retrieval event should be logged for compliance:
            ```python
            audit_log.write({
                "timestamp":   datetime.utcnow(),
                "user_id":     current_user.id,
                "query":       query,
                "retrieved":   [c.id for c in chunks],
                "scores":      [c.score for c in chunks],
                "answer_hash": sha256(answer),
            })
            ```
            """
        )

    with tab2:
        st.markdown(
            """
            #### Distributed Vector Databases

            | Need | Solution |
            |------|----------|
            | < 1M vectors | Single Qdrant node / Qdrant Cloud |
            | 1M–100M vectors | Qdrant cluster (sharding) or Weaviate |
            | 100M+ vectors | Qdrant + PQ quantisation + on-disk storage |
            | Multi-region | Qdrant Cloud multi-region replicas |

            #### Caching Strategies

            **Embedding cache** — avoid re-embedding the same document text:
            ```python
            import hashlib, redis

            def get_embedding(text: str) -> list[float]:
                key = "emb:" + hashlib.md5(text.encode()).hexdigest()
                cached = redis_client.get(key)
                if cached:
                    return json.loads(cached)
                vec = embed_model.encode(text).tolist()
                redis_client.setex(key, 86400, json.dumps(vec))  # TTL 24h
                return vec
            ```

            **LLM response cache** — identical queries return instantly:
            ```python
            def cached_rag(query: str) -> str:
                key = "rag:" + hashlib.md5(query.encode()).hexdigest()
                if hit := redis_client.get(key):
                    return json.loads(hit)
                result = run_rag(query)
                redis_client.setex(key, 3600, json.dumps(result))  # TTL 1h
                return result
            ```

            **Result:** 60–80% of repeat queries served from cache at near-zero cost.

            #### Batch Ingestion Pipeline
            ```python
            # Don't embed one-by-one — batch for 10x throughput
            BATCH_SIZE = 64
            for i in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[i : i + BATCH_SIZE]
                vectors = embed_model.encode(
                    [c["text"] for c in batch],
                    batch_size=BATCH_SIZE,
                    show_progress_bar=True,
                )
                client.upsert(collection_name="kb", points=[...])
            ```
            """
        )

    with tab3:
        st.markdown(
            """
            #### What to Track in Every RAG Call

            ```python
            @dataclass
            class RAGTrace:
                query:             str
                expanded_query:    str | None
                retrieved_chunks:  list[str]   # chunk IDs
                retrieval_scores:  list[float]
                reranked_scores:   list[float] | None
                context_tokens:    int
                answer:            str
                faithfulness:      float | None  # from RAGAS
                latency_ms:        float
                cost_usd:          float
                failure_mode:      str | None    # "no_chunks" | "low_scores" | "hallucinated"
            ```

            #### Tracing Common Failure Modes

            | Symptom | Root cause | Fix |
            |---------|------------|-----|
            | Score < 0.5 for all chunks | Query too vague | Apply query expansion |
            | Score > 0.8 but wrong answer | Wrong chunks retrieved | Check chunking strategy |
            | Right chunks, hallucinated answer | LLM ignoring context | Tighten system prompt |
            | Correct answer, missing citation | Prompt doesn't ask for citation | Update prompt template |
            | Timeout | Context too long | Apply LLMLingua compression |
            | Same query, different answers | No caching + LLM temperature > 0 | Cache + set temperature=0 |

            #### Visualising Retrieval Health (Streamlit snippet)
            ```python
            avg_score = mean(scores)
            if avg_score < 0.5:
                st.error("🔴 Low retrieval quality — query expansion recommended")
            elif avg_score < 0.7:
                st.warning("🟡 Medium quality — consider reranking")
            else:
                st.success("🟢 Good retrieval quality")
            ```
            """
        )

    with tab4:
        st.markdown(
            """
            #### Four Levers to Pull on RAG Cost

            **Lever 1 — Embedding cache** (biggest win for repeated queries)
            Save computed embeddings; a cache hit costs $0.00 vs ~$0.0001 per embed.

            **Lever 2 — Sparse + dense mix**
            BM25 / TF-IDF keyword search is *free* (no API call).
            Run sparse first; only escalate to dense embedding when sparse
            returns < 3 good results.

            **Lever 3 — Context compression (LLMLingua)**
            Cutting context from 3,000 → 900 tokens cuts the LLM call cost by 70%.

            **Lever 4 — Model tiering**
            ```
            Simple factual query    → gpt-4o-mini   ($0.15/1M tokens)
            Complex synthesis       → gpt-4o        ($2.50/1M tokens)
            Internal/confidential   → local Ollama  ($0.00)
            ```

            #### Cost per query breakdown (example)
            | Component | Cost |
            |-----------|------|
            | Embedding (query) | $0.000013 |
            | Qdrant vector search | ~$0.00 (included in plan) |
            | LLM (gpt-4o-mini, 1K tokens) | $0.00015 |
            | **Total per query** | **~$0.00017** |
            | At 10,000 queries/day | **~$1.70/day** |

            Caching 70% of repeat queries → **$0.51/day** — 70% saving.
            """
        )


# ── Section 6: RAGAS Evaluation ───────────────────────────────────────────────

def _section_ragas() -> None:
    st.markdown("### 📊 RAGAS Evaluation — Measuring RAG Quality")

    st.markdown(
        """
        **RAGAS** (Retrieval Augmented Generation Assessment) is the standard
        framework for evaluating RAG systems. It measures four dimensions:
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            #### 📌 Faithfulness
            *Is the answer grounded in the retrieved documents?*

            Score = 0 means the LLM hallucinated — it gave an answer
            that cannot be traced back to any retrieved chunk.

            Score = 1 means every claim in the answer is directly
            supported by the retrieved context.

            ```python
            # RAGAS will check each sentence in the answer:
            # "Aspirin can cause gastric bleeding"  ← present in chunk 2? ✓
            # "Aspirin was invented in 1897"        ← present in any chunk? ✗
            # Faithfulness = 1/2 = 0.5
            ```
            """
        )
        st.markdown(
            """
            #### 🎯 Answer Relevance
            *Does the answer actually address the question asked?*

            RAGAS generates N alternative questions that the answer could
            belong to, then checks if the original question is among them.

            Low score = the answer is factually correct but off-topic
            (e.g. asked about aspirin dosage, answered about ibuprofen).
            """
        )

    with col2:
        st.markdown(
            """
            #### 🔬 Context Precision
            *Are the retrieved chunks actually useful?*

            Of the K chunks you retrieved, what fraction genuinely
            contributed to the answer?

            If you retrieved 5 chunks and only 2 were relevant:
            `Context Precision = 2/5 = 0.4`

            Low score → over-retrieval, noisy context, threshold too low.
            """
        )
        st.markdown(
            """
            #### 🗂️ Context Recall
            *Did you retrieve enough to answer fully?*

            Checks whether the ground-truth answer could be reconstructed
            from the retrieved chunks.

            Low score → under-retrieval, chunks too small, relevant docs
            not ingested, or top-K too low.
            """
        )

    st.markdown("---")
    st.markdown("#### Running RAGAS in Python")
    st.code(
        """
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# Build evaluation dataset
data = {
    "question":   ["What is the GDPR fine limit?"],
    "answer":     ["The maximum fine is €20 million or 4% of global turnover."],
    "contexts":   [["Article 83(5) GDPR sets the maximum fine at €20M or 4% annual turnover..."]],
    "ground_truth": ["GDPR fines can reach €20 million or 4% of global annual turnover."],
}
dataset = Dataset.from_dict(data)

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
)
print(result)
# {'faithfulness': 0.96, 'answer_relevancy': 0.94,
#  'context_precision': 0.88, 'context_recall': 0.91}
""",
        language="python",
    )

    with st.expander("🎯 What score targets should you aim for?"):
        import pandas as pd
        df = pd.DataFrame({
            "Metric": ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall"],
            "< 0.7 (Poor)": ["Hallucinating regularly", "Off-topic answers", "Retrieval too noisy", "Missing key docs"],
            "0.7–0.85 (Acceptable)": ["Occasional errors", "Mostly on-topic", "Some noise", "Mostly complete"],
            "> 0.85 (Production-ready)": ["Trustworthy", "Highly relevant", "Clean retrieval", "Comprehensive"],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)


# ── Section 7: Common Pitfalls ────────────────────────────────────────────────

def _section_pitfalls() -> None:
    st.markdown("### ⚠️ Common Pitfalls — What Breaks RAG in Production")

    pitfalls = [
        (
            "❌ Chunking too large",
            "**Symptom:** Low context precision score. The LLM gets 2,000-token chunks "
            "and the relevant sentence is buried in paragraph 8.\n\n"
            "**Fix:** Target 256–512 tokens per chunk. Use semantic chunking to split "
            "at meaning boundaries rather than arbitrary token counts.",
        ),
        (
            "❌ Chunking too small",
            "**Symptom:** Retrieved chunks are correct but the LLM says 'insufficient information'. "
            "Each 64-token chunk is too granular — half a sentence without context.\n\n"
            "**Fix:** Minimum 128 tokens per chunk. Add 20% overlap. Include section "
            "header as prefix metadata in every chunk.",
        ),
        (
            "❌ No reranking",
            "**Symptom:** You retrieve top-10 and pass all 10 to the LLM. "
            "Only 3 are genuinely relevant. The LLM hallucinates to reconcile the noise.\n\n"
            "**Fix:** Add a cross-encoder reranker after cosine retrieval. "
            "Pass only top-3 to the LLM. Fewer, better chunks beat more, noisier ones.",
        ),
        (
            "❌ Blind retrieval (no verification)",
            "**Symptom:** When the answer is not in the knowledge base, "
            "the LLM invents one that sounds plausible.\n\n"
            "**Fix:** Add a relevance gate — if max score < 0.5, tell the LLM "
            "*'No relevant documents found'* rather than passing empty/low-quality context. "
            "Implement Corrective RAG: check quality → fallback to web search if needed.",
        ),
        (
            "❌ No evaluation (shipping broken RAG by accident)",
            "**Symptom:** You deploy, users complain, you have no idea what went wrong "
            "because you never measured faithfulness or relevance.\n\n"
            "**Fix:** Run RAGAS on 50–100 representative Q&A pairs before every deploy. "
            "Set a minimum bar: faithfulness > 0.85. Fail the CI pipeline if it drops below.",
        ),
        (
            "❌ Stale embeddings",
            "**Symptom:** Documents are updated but the old vectors stay in the DB. "
            "The LLM cites outdated policies.\n\n"
            "**Fix:** Attach `last_updated` metadata to every chunk. "
            "Run a nightly job that deletes and re-embeds changed documents. "
            "Filter retrieval by `date > cutoff` for time-sensitive domains.",
        ),
        (
            "❌ Ignoring the system prompt",
            "**Symptom:** The LLM has perfect context but still makes things up — "
            "because the system prompt says 'answer helpfully' with no grounding constraint.\n\n"
            "**Fix:** System prompt must say: *'Answer ONLY using the provided context. "
            "If the answer is not in the context, say so.'* Add: *'Do not use your training knowledge.'*",
        ),
    ]

    for title, body in pitfalls:
        with st.expander(title):
            st.markdown(body)


# ── Section 8: Real-World Problem Statements ─────────────────────────────────

def _section_problem_statements() -> None:
    st.markdown("### 🎯 Real-World RAG Problem Statements")
    st.info(
        "**Session exercise:** For each scenario below, identify which RAG architecture, "
        "chunking strategy, retrieval technique, and safety mechanisms you would apply. "
        "Answers will be discussed live."
    )

    ps1, ps2, ps3, ps4 = st.tabs([
        "🏦 Financial Services",
        "💻 SaaS Support",
        "🏭 Enterprise Knowledge",
        "🏥 Healthcare",
    ])

    with ps1:
        st.markdown(
            """
            #### Problem Statement 1: UK Bank — Compliance & Risk

            A major UK bank (1,000+ employees) has:
            - **50,000+ regulatory documents** (FCA guidance, internal policies, precedent decisions)
            - **200+ loan officers** making decisions daily
            - **Audit requirement:** every decision must cite which policy was applied
            - **Current state:** officers manually search SharePoint, find wrong/outdated docs, cite from memory

            ---

            #### What They Face

            - ❌ Wrong policy cited → audit failure → **£50K fine per instance**
            - ❌ Officer searches for 30 minutes, still doesn't find the relevant policy
            - ❌ Two officers give different answers to the same question (inconsistency)
            - ❌ When regulations change, old docs aren't retired — officers still cite them

            ---

            #### Questions to Consider
            """
        )
        for q in [
            "Which RAG architecture would you choose? Why not Naive RAG?",
            "How would you handle document versioning (old vs updated policies)?",
            "What metadata would you attach to each chunk?",
            "How do you ensure every answer includes a verifiable citation?",
            "What happens when a new FCA regulation is published overnight?",
        ]:
            st.markdown(f"- {q}")

    with ps2:
        st.markdown(
            """
            #### Problem Statement 2: SaaS Company — Customer Support at Scale

            A 500-person SaaS company (CRM software):
            - **100,000+ support articles** across 15 product versions
            - **50 support agents** handling 200+ tickets/day
            - **Current state:** agents Google/search internally, find outdated info, give wrong answers

            ---

            #### What They Face

            - ❌ Customers complain: *"Your support gave me the wrong answer"*
            - ❌ Agent spends 10 mins searching per ticket → handles only 15 tickets/day (target: 30+)
            - ❌ New agents take 3 weeks to learn the product — can't find relevant docs
            - ❌ When docs update, old answers persist in chat history — customers confused
            - ❌ *"Why does agent John always resolve faster?"* → he knows the docs better than the system

            ---

            #### Questions to Consider
            """
        )
        for q in [
            "How would you handle 15 different product versions in one knowledge base?",
            "What chunking strategy suits support articles (FAQs, step-by-step guides)?",
            "How do you prevent stale answers after a doc update?",
            "How would RAGAS evaluation work for support tickets?",
            "What caching strategy would halve the average handle time?",
        ]:
            st.markdown(f"- {q}")

    with ps3:
        st.markdown(
            """
            #### Problem Statement 3: Manufacturing Company — Fragmented Knowledge

            A 5,000-person manufacturing company:
            - **100,000 PDFs** scattered: SOPs, equipment manuals, incident reports, design specs, training video transcripts
            - Across **SharePoint, Google Drive, OneDrive, Teams, old FTP servers**
            - Engineers working on a new production line need: *"How did we solve this problem before?"*
            - **Current state:** ask colleagues — no searchable record

            ---

            #### What They Face

            - ❌ Same problems solved 3 different ways (no institutional knowledge)
            - ❌ When an engineer leaves, their 10 years of know-how leaves with them
            - ❌ Repeated mistakes: *"We already solved this in 2019"*
            - ❌ Onboarding takes 6 months (learning by osmosis, not documentation)
            - ❌ Different facilities solve the same problem differently (no consistency)

            ---

            #### Questions to Consider
            """
        )
        for q in [
            "How do you ingest documents from 5 different storage systems?",
            "What metadata is critical for a manufacturing knowledge base?",
            "How would you handle scanned PDFs (image-only) with no searchable text?",
            "How do you surface 'we solved this in 2019' when the engineer doesn't know the right keywords?",
            "What access control pattern prevents a contractor from seeing confidential design specs?",
        ]:
            st.markdown(f"- {q}")

    with ps4:
        st.markdown(
            """
            #### Problem Statement 4: Hospital System — Clinical Decision Support

            A hospital system with 50 facilities:
            - Doctors need instant access to drug interactions, contraindications, latest treatment protocols
            - **Current state:** doctors manually look up Micromedex + internal protocols + consult colleagues

            ---

            #### What They Face

            - ❌ Drug-drug interaction missed → **patient harm → liability**
            - ❌ Doctor prescribes outdated protocol → worse patient outcomes
            - ❌ ER doctor doesn't know this patient was treated for a rare condition 2 years ago at another facility
            - ❌ Discharge checklist is vague — steps are sometimes missed

            ---

            #### Questions to Consider
            """
        )
        for q in [
            "Medical accuracy is life-critical. Which RAG architecture (from the 8 types) do you choose?",
            "What safety mechanisms prevent a hallucinated drug dosage from reaching a doctor?",
            "How do you handle a contradiction between two retrieved sources (old vs new protocol)?",
            "What confidence threshold would you set before showing an answer vs escalating to a human?",
            "How do you evaluate this system? What RAGAS score is 'good enough' for clinical use?",
        ]:
            st.markdown(f"- {q}")

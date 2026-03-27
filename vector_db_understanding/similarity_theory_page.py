"""Streamlit page: cohort-style similarity math (plain language + formulas + worked examples)."""

from __future__ import annotations

import math

import streamlit as st

from similarity_math import (
    cosine_similarity,
    dot_product,
    euclidean_distance,
    manhattan_distance,
)


def show_similarity_math_theory() -> None:
    st.markdown(
        '<h2 class="section-header">📐 Similarity math — theory & worked examples</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        Speaker-style notes: each metric answers a **different question** about two vectors.
        Use the interactive **Similarity Metrics** page next to play with sliders; this page is the **math story**.
        """
    )

    st.markdown("### The mental model")
    st.markdown(
        """
        - A **vector** is a list of numbers — an arrow from the origin into space (2D, 3D, or thousands of dimensions for embeddings).
        - **Similarity / distance** measures how “close” two vectors are. Meaning depends on the metric.
        - **Distances** (Euclidean, Manhattan): *smaller* = closer. **Scores** (cosine, dot): *higher* often means more aligned — but dot product also grows with length.
        """
    )

    st.divider()

    st.markdown("### Dot product — “How much do these two lists reinforce each other?”")
    st.markdown(
        """
        **Intuition:** Multiply each pair of matching coordinates and add. Large values in the same dimension with the **same sign** push the sum up.
        """
    )
    st.latex(r"\mathbf{a} \cdot \mathbf{b} = \sum_i a_i b_i")
    st.markdown(
        """
        **Worked example:** $\\mathbf{a} = [2, 3]$, $\\mathbf{b} = [4, 1]$ → Dot $= 2 \\times 4 + 3 \\times 1 = 11$.

        **In words:** Agreement dimension by dimension — no “angle” yet, just weighted overlap.

        **Note:** Raw dot product grows with vector length; for search we often use **normalized** vectors or **cosine**.
        """
    )
    _verify_row(
        "Check",
        {
            "dot([2,3], [4,1])": dot_product([2.0, 3.0], [4.0, 1.0]),
        },
    )

    st.divider()

    st.markdown("### Cosine similarity — “Do the two arrows point in the same direction?”")
    st.markdown(
        """
        **Intuition:** Ignore arrow **length**; use the **angle**. $[0.9, 0.1]$ and $[0.45, 0.05]$ are parallel (same taste), even if the second is “quieter.”
        """
    )
    st.latex(
        r"\mathrm{cos\_sim}(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \,\|\mathbf{b}\|}"
    )
    st.latex(r"\|\mathbf{a}\| = \sqrt{\sum_i a_i^2}")
    st.markdown(
        """
        **Range:** typically **[-1, 1]**. **1** = same direction, **0** = orthogonal, **-1** = opposite.

        **Worked example:** $\\mathbf{a} = [1, 0]$, $\\mathbf{b} = [1, 1]$ → cosine $= 1/\\sqrt{2} \\approx 0.707$.

        **Cosine distance** (used in some DBs): $1 - \\mathrm{cos\\_sim}$ (smaller = closer).
        """
    )
    cs = cosine_similarity([1.0, 0.0], [1.0, 1.0])
    _verify_row(
        "Check",
        {
            "cos_sim([1,0], [1,1])": cs,
            "1/√2": 1 / math.sqrt(2),
        },
    )

    st.divider()

    st.markdown("### Euclidean distance (L2) — “Straight-line distance in space”")
    st.markdown(
        """
        **Intuition:** Ruler distance between points. Use when **scale / magnitude** matters (prices, coordinates).
        """
    )
    st.latex(r"\|\mathbf{a} - \mathbf{b}\|_2 = \sqrt{\sum_i (a_i - b_i)^2}")
    st.markdown(
        """
        **Worked example:** $[0,0]$ to $[3,4]$ → $\\sqrt{3^2 + 4^2} = 5$ (3–4–5 triangle).
        """
    )
    _verify_row(
        "Check",
        {"euclidean([0,0], [3,4])": euclidean_distance([0.0, 0.0], [3.0, 4.0])},
    )

    st.divider()

    st.markdown("### Manhattan distance (L1) — “City-block distance”")
    st.markdown(
        """
        **Intuition:** Move only along axes; sum **absolute** differences. Robust when one **outlier** dimension shouldn’t dominate (Euclidean **squares** big gaps).
        """
    )
    st.latex(r"\|\mathbf{a} - \mathbf{b}\|_1 = \sum_i |a_i - b_i|")
    st.markdown(
        """
        **Worked example:** $[1,2]$ vs $[4,6]$ → $|1-4| + |2-6| = 7$.
        """
    )
    _verify_row(
        "Check",
        {"manhattan([1,2], [4,6])": manhattan_distance([1.0, 2.0], [4.0, 6.0])},
    )

    st.divider()

    st.markdown("### Quick comparison (slide table)")
    st.markdown(
        """
        | Question | Metric | “More similar” means… |
        |------------|--------|------------------------|
        | Same direction / normalized embeddings? | **Cosine** | Score closer to **1** |
        | Straight-line gap? | **Euclidean** | **Smaller** distance |
        | Axis-only (city block) gap? | **Manhattan** | **Smaller** distance |
        | Raw weighted overlap? | **Dot product** | Often larger — but **scale** matters |
        """
    )

    st.markdown("### How this ties to Qdrant / vector search")
    st.info(
        """
        Many pipelines **normalize** embeddings (length 1). Then **dot product = cosine similarity** for ranking neighbors.

        In Qdrant, pick a **distance** that matches how your vectors were built (cosine, dot, Euclidean, …).
        """
    )


def _verify_row(title: str, values: dict[str, float]) -> None:
    with st.expander(f"🧮 {title} (same formulas as `similarity_math.py`)"):
        cols = st.columns(len(values))
        for col, (label, val) in zip(cols, values.items()):
            col.metric(label, f"{val:.6f}" if isinstance(val, float) else str(val))

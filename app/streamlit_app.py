import sys
from pathlib import Path

# Make project root available for `from app...` imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.api.routes import get_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Agentic RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #777;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }

    .status-card {
        padding: 12px 16px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }

    .step-card {
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }

    .step-title {
        font-size: 1.05rem;
        font-weight: 650;
    }

    .small-text {
        color: #777;
        font-size: 0.9rem;
    }

    .source-chip {
        display: inline-block;
        padding: 6px 10px;
        margin: 4px;
        border-radius: 8px;
        background: rgba(100, 100, 100, 0.10);
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 Agentic RAG")

    st.caption("Software Engineering QA")

    st.divider()

    st.markdown("### System")

    st.success("● Agent Ready")
    st.success("● FastAPI Backend")
    st.success("● Qdrant Retrieval")
    st.success("● Ollama LLM")

    st.divider()

    st.markdown("### Model")

    st.write("**Mistral 7B**")

    st.markdown("### Vector Database")

    st.write("**Qdrant**")

    st.markdown("### Retrieval")

    st.write("**Embeddings + Vector Search**")

    st.divider()

    st.caption(
        "Agentic RAG routes questions, retrieves "
        "repository context, evaluates relevance, "
        "and can fall back to web search."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Agentic RAG</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Software Engineering Question Answering"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_area(
    "Ask a question",
    placeholder=(
        "e.g. How does FastAPI define an API route?"
    ),
    height=110,
)


ask = st.button(
    "🔎  Ask Agent",
    type="primary",
    use_container_width=True,
)


# ============================================================
# EXECUTION
# ============================================================

if ask:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Agent is routing, retrieving and reasoning..."
        ):

            pipeline = get_pipeline()
            result = pipeline.run(question)

        # --------------------------------------------------------
        # EXTRACT RESULT
        # --------------------------------------------------------

        route = result.get("route", "unknown")
        score = result.get("retrieval_score", 0)
        retries = result.get("retry_count", 0)
        web_used = result.get("web_search_used", False)

        documents = result.get("documents", [])
        web_documents = result.get("web_documents", [])
        rewritten_query = result.get("rewritten_query")

        answer = result.get(
            "answer",
            "No answer generated.",
        )

        # ========================================================
        # ANSWER
        # ========================================================

        st.markdown("## 💡 Answer")

        st.markdown(answer)

        st.divider()

        # ========================================================
        # QUICK METRICS
        # ========================================================

        st.markdown("## 📊 Execution Overview")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Route",
                route.upper(),
            )

        with c2:
            st.metric(
                "Retrieved",
                len(documents),
            )

        with c3:
            st.metric(
                "Retries",
                retries,
            )

        with c4:
            st.metric(
                "Web Search",
                "YES" if web_used else "NO",
            )

        st.divider()

        # ========================================================
        # AGENT TRACE
        # ========================================================

        st.markdown("## 🤖 Agent Execution")

        # --------------------------------------------------------
        # STEP 1
        # --------------------------------------------------------

        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">
                    👤 1. User Query
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(question)

        st.markdown(
            "<center>↓</center>",
            unsafe_allow_html=True,
        )

        # --------------------------------------------------------
        # STEP 2
        # --------------------------------------------------------

        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">
                    🧭 2. Query Router
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if route == "direct":

            st.success(
                "DIRECT — General knowledge question. "
                "Repository retrieval skipped."
            )

        elif route == "retrieve":

            st.info(
                "RETRIEVE — Repository context is likely "
                "useful for answering this question."
            )

        elif route == "complex":

            st.warning(
                "COMPLEX — The agent determined that "
                "deeper investigation is required."
            )

        else:

            st.info(
                f"Router selected: **{route}**"
            )

        # ========================================================
        # RETRIEVAL BRANCH
        # ========================================================

        if route != "direct":

            st.markdown(
                "<center>↓</center>",
                unsafe_allow_html=True,
            )

            # ----------------------------------------------------
            # STEP 3 — RETRIEVAL
            # ----------------------------------------------------

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-title">
                        🔎 3. Vector Retrieval
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            r1, r2 = st.columns(2)

            with r1:

                st.metric(
                    "Documents Retrieved",
                    len(documents),
                )

            with r2:

                st.metric(
                    "Retrieval Score",
                    score,
                )

            if documents:

                st.success(
                    f"Retrieved {len(documents)} "
                    "repository document(s)."
                )

                st.markdown("#### 📚 Retrieved Sources")

                for i, doc in enumerate(
                    documents,
                    start=1,
                ):

                    if isinstance(doc, dict):

                        metadata = doc.get(
                            "metadata",
                            {},
                        )

                    else:

                        metadata = {}

                    source = metadata.get(
                        "source",
                        f"Repository Document {i}",
                    )

                    file_type = metadata.get(
                        "file_type",
                        "",
                    )

                    label = source

                    if file_type:

                        label += (
                            f" · {file_type}"
                        )

                    st.markdown(
                        f'<span class="source-chip">'
                        f"📄 {label}"
                        f"</span>",
                        unsafe_allow_html=True,
                    )

                # Optional context
                with st.expander(
                    "📖 View retrieved context"
                ):

                    for i, doc in enumerate(
                        documents,
                        start=1,
                    ):

                        if isinstance(doc, dict):

                            content = doc.get(
                                "content",
                                "",
                            )

                            metadata = doc.get(
                                "metadata",
                                {},
                            )

                        else:

                            content = str(doc)
                            metadata = {}

                        st.markdown(
                            f"**Document {i}**"
                        )

                        if metadata:

                            st.caption(
                                str(metadata)
                            )

                        st.code(
                            content,
                            language="text",
                        )

            else:

                st.warning(
                    "No repository documents were retrieved."
                )

            # ----------------------------------------------------
            # STEP 4 — GRADER
            # ----------------------------------------------------

            st.markdown(
                "<center>↓</center>",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-title">
                        🎯 4. Retrieval Grader
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if score and score > 0:

                st.success(
                    f"✓ Relevant context found "
                    f"(score: {score})"
                )

            else:

                st.warning(
                    "⚠ Low retrieval relevance."
                )

            # ----------------------------------------------------
            # STEP 5 — REWRITE / RETRY
            # ----------------------------------------------------

            if retries > 0 or rewritten_query:

                st.markdown(
                    "<center>↓</center>",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    """
                    <div class="step-card">
                        <div class="step-title">
                            🔄 5. Query Rewrite / Retry
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.warning(
                    f"The agent performed "
                    f"{retries} retrieval retry(s)."
                )

                if rewritten_query:

                    with st.expander(
                        "View rewritten query"
                    ):

                        st.markdown(
                            "**Original Query**"
                        )

                        st.code(
                            question,
                            language="text",
                        )

                        st.markdown(
                            "**Rewritten Query**"
                        )

                        st.code(
                            rewritten_query,
                            language="text",
                        )

            # ----------------------------------------------------
            # STEP 6 — WEB SEARCH
            # ----------------------------------------------------

            st.markdown(
                "<center>↓</center>",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="step-card">
                    <div class="step-title">
                        🌐 6. Web Search
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if web_used:

                st.success(
                    f"Web search triggered — "
                    f"{len(web_documents)} result(s)."
                )

                if web_documents:

                    with st.expander(
                        "View web sources"
                    ):

                        for i, doc in enumerate(
                            web_documents,
                            start=1,
                        ):

                            if isinstance(doc, dict):

                                title = doc.get(
                                    "title",
                                    f"Web Result {i}",
                                )

                                url = doc.get(
                                    "url",
                                    "",
                                )

                                content = doc.get(
                                    "content",
                                    "",
                                )

                            else:

                                title = (
                                    f"Web Result {i}"
                                )

                                url = ""
                                content = str(doc)

                            st.markdown(
                                f"**{i}. {title}**"
                            )

                            if url:

                                st.caption(url)

                            if content:

                                st.write(
                                    content
                                )

            else:

                st.info(
                    "Not required — repository "
                    "context was sufficient."
                )

        else:

            st.markdown(
                "<center>↓</center>",
                unsafe_allow_html=True,
            )

            st.info(
                "⏭️ Retrieval skipped because the "
                "router selected the DIRECT path."
            )

        # ========================================================
        # FINAL GENERATION
        # ========================================================

        st.markdown(
            "<center>↓</center>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">
                    💬 Final Answer Generation
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.success(
            "✓ Agent completed the reasoning pipeline "
            "and generated the final answer."
        )

        # ========================================================
        # DEVELOPER DETAILS
        # ========================================================

        st.divider()

        with st.expander(
            "🔧 Developer Details"
        ):

            st.json(
                {
                    "route": route,
                    "retrieval_score": score,
                    "retry_count": retries,
                    "web_search_used": web_used,
                    "documents_retrieved": len(
                        documents
                    ),
                    "web_documents_retrieved": len(
                        web_documents
                    ),
                    "rewritten_query": (
                        rewritten_query
                    ),
                }
            )
import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


st.set_page_config(
    page_title="Agentic RAG",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agentic RAG")
st.caption("Software Engineering Question Answering")


question = st.text_area(
    "Ask a question",
    placeholder="e.g. How does FastAPI define an API route?",
    height=100,
)


if st.button("🔍 Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": question},
                    timeout=120,
                )
                response.raise_for_status()
                result = response.json()

                st.subheader("Answer")
                st.markdown(result["answer"])

                st.divider()

                st.subheader("Agent Details")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Route", result["route"])

                with col2:
                    st.metric("Retrieval Score", result["retrieval_score"])

                with col3:
                    st.metric("Retries", result["retry_count"])

                with col4:
                    st.metric(
                        "Web Search",
                        "Yes" if result["web_search_used"] else "No",
                    )

            except requests.RequestException as e:
                st.error(f"Backend request failed: {e}")
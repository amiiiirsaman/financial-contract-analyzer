import os
import streamlit as st

from core.rag_service import RAGService, RAGConfig

# --- Config from env for deployability ---
KB_ID = os.getenv("KB_ID", "HHFPLNTGBM")
GUARDRAIL_ID = os.getenv("GUARDRAIL_ID")
GUARDRAIL_VERSION = os.getenv("GUARDRAIL_VERSION")

rag_service = RAGService(
    RAGConfig(
        knowledge_base_id=KB_ID,
        guardrail_id=GUARDRAIL_ID,
        guardrail_version=GUARDRAIL_VERSION,
    )
)

st.set_page_config(page_title="Financial Contract Analyzer", layout="wide")
st.title("📄 Financial Contract Analyzer (Bedrock RAG)")

if "session_id" not in st.session_state:
    st.session_state.session_id = st.session_state.get("_session_id", "local-session")

with st.sidebar:
    st.header("Session")
    if st.button("New session"):
        st.session_state.session_id = os.urandom(8).hex()
    st.write(f"Session ID: `{st.session_state.session_id}`")

prompt = st.text_area("Ask about your contracts", height=150)

if st.button("Analyze") and prompt.strip():
    with st.spinner("Querying knowledge base..."):
        answer = rag_service.get_response(prompt)
    st.subheader("Answer")
    st.write(answer)

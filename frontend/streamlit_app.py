import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="YogeAI Document Assistant", page_icon="📚")
st.title(" YogeAI Document Assistant")
st.write("Upload a text-based PDF, then ask a question grounded in its contents.")

with st.sidebar:
    st.markdown("### Workflow")
    st.markdown("1. Upload a PDF\n2. Index its text\n3. Ask a question\n4. Inspect source pages")
    st.caption("Starter version: local in-memory index; restart clears indexed data.")

uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
if uploaded and st.button("Upload and index", type="primary"):
    try:
        with st.spinner("Uploading and indexing..."):
            response = requests.post(
                f"{API_URL}/documents",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                timeout=180,
            )
        if response.ok:
            st.session_state["last_ingested"] = response.json()
            st.success(f"Indexed {response.json()['chunks_indexed']} chunks.")
            st.json(response.json())
        else:
            st.error(response.text)
    except requests.RequestException as exc:
        st.error(f"Cannot reach the API. Start FastAPI first. Details: {exc}")

question = st.text_input("Ask a question", placeholder="What is the refund window?")
top_k = st.slider("Number of passages to retrieve", 1, 8, 4)
if st.button("Ask", disabled=not question.strip()):
    try:
        with st.spinner("Searching and generating an answer..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question, "top_k": top_k},
                timeout=120,
            )
        if response.ok:
            result = response.json()
            st.subheader("Answer")
            st.write(result["answer"])
            st.subheader("Retrieved sources")
            for i, source in enumerate(result["sources"], start=1):
                with st.expander(
                    f"Source {i}: {source['document_name']} — page {source['page']} "
                    f"(score {source['score']:.3f})"
                ):
                    st.write(source["text"])
        else:
            st.error(response.text)
    except requests.RequestException as exc:
        st.error(f"Cannot reach the API. Start FastAPI first. Details: {exc}")

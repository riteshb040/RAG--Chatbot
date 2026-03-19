import streamlit as st
import tempfile
import os
from rag import ChatPDF

st.set_page_config(page_title="Simple ChatPDF", page_icon="📄")

# Initialize
if "chatpdf" not in st.session_state:
    st.session_state.chatpdf = ChatPDF()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ingested" not in st.session_state:
    st.session_state.ingested = False

st.title("📄 Chat with PDF (Simple RAG)")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📁 Upload PDF")
    uploaded_file = st.file_uploader("Upload a PDF to chat with it", type="pdf")

    if uploaded_file:
        if not st.session_state.ingested:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                file_path = tmp.name

            with st.spinner("Processing PDF..."):
                st.session_state.chatpdf.ingest(file_path)
            os.remove(file_path)
            st.success("PDF processed! ✅")
            st.session_state.ingested = True

    if st.button("🗑️ Clear PDF & Chat"):
        st.session_state.chatpdf.clear()
        st.session_state.messages = []
        st.session_state.ingested = False
        st.rerun()

    st.divider()
    if st.session_state.ingested:
        st.info("📗 **Mode: PDF Q&A**\nAsking questions from your PDF.")
    else:
        st.info("💬 **Mode: Normal Chat**\nNo PDF uploaded. Chatting freely.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if query := st.chat_input("Ask a question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    # Get response based on mode
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.ingested:
                answer = st.session_state.chatpdf.ask(query)
            else:
                answer = st.session_state.chatpdf.chat(query)
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

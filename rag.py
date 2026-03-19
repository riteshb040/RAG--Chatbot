import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.chat_models import ChatOllama


class ChatPDF:
    def __init__(self):
        self.vector_store = None
        self.retriever = None
        self.model = ChatOllama(model="llama3")

    def ingest(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        docs = splitter.split_documents(documents)

        embeddings = FastEmbedEmbeddings()
        self.vector_store = Chroma.from_documents(docs, embeddings)

        self.retriever = self.vector_store.as_retriever()

    def ask(self, query):
        if not self.retriever:
            return {"answer": "Upload PDF first!", "retrieval_time": 0, "llm_time": 0, "total_time": 0}

        total_start = time.time()

        # Measure retrieval time
        retrieval_start = time.time()
        docs = self.retriever.invoke(query)
        retrieval_time = time.time() - retrieval_start

        if not docs:
            return {"answer": "No answer found in document.", "retrieval_time": retrieval_time, "llm_time": 0, "total_time": time.time() - total_start}

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

        # Measure LLM response time
        llm_start = time.time()
        response = self.model.invoke(prompt)
        llm_time = time.time() - llm_start

        total_time = time.time() - total_start

        return {
            "answer": response.content,
            "retrieval_time": round(retrieval_time, 2),
            "llm_time": round(llm_time, 2),
            "total_time": round(total_time, 2)
        }

    def chat(self, query):
        """Normal chatbot mode — no PDF needed."""
        start = time.time()
        response = self.model.invoke(query)
        llm_time = time.time() - start

        return {
            "answer": response.content,
            "retrieval_time": 0,
            "llm_time": round(llm_time, 2),
            "total_time": round(llm_time, 2)
        }

    def clear(self):
        self.vector_store = None
        self.retriever = None
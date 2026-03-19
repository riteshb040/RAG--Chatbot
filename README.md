# Local RAG: Private Chat with your PDFs 📄🤖

A professional, local-first Retrieval-Augmented Generation (RAG) application built with **LangChain**, **Streamlit**, and **Ollama**. This project allows you to chat with your PDF documents privately on your own machine, with real-time performance tracking.

![Project Screenshot]("images/Screenshot1.png")

## 🌟 Key Features

- **Dual-Mode Chat**: 
  - 📗 **PDF Q&A Mode**: Ask questions specifically about your uploaded document.
  - 💬 **General Chat Mode**: Talk to the LLM directly for general knowledge without needing a PDF.
- **Local & Private**: Your data never leaves your machine. Everything runs locally using Ollama and FastEmbed.
- **Performance Tracking**: Built-in latency metrics showing time taken for Retrieval, LLM generation, and Total response time.
- **Modern UI**: Clean, ChatGPT-like interface built with Streamlit.
- **Session Management**: Chat history is preserved during your session.

## 🚀 Getting Started

### Prerequisites

1.  **Ollama**: Install from [ollama.com](https://ollama.com).
2.  **LLM Model**: Pull the Llama 3 model:
    ```bash
    ollama pull llama3
    ```

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/riteshb040/RAG--Chatbot.git
    cd local-rag
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

```bash
streamlit run main.py
```

## 🛠️ Built With

- **[LangChain](https://www.langchain.com/)**: Framework for LLM application development.
- **[Streamlit](https://streamlit.io/)**: For the interactive web interface.
- **[Ollama](https://ollama.ai/)**: For running large language models locally.
- **[ChromaDB](https://www.trychroma.com/)**: Fast, open-source vector database.
- **[FastEmbed](https://github.com/qdrant/fastembed)**: Efficient local embeddings generation.

## 🏗️ Architecture Overview

1.  **Ingestion**: PDFs are loaded using `PyPDFLoader`, split into chunks with `CharacterTextSplitter`, and embedded using `FastEmbedEmbeddings`.
2.  **Storage**: Vector embeddings are stored in a local `Chroma` database (stored in `.chroma/`).
3.  **Retrieval**: When a question is asked, the most relevant chunks are retrieved using semantic search.
4.  **Generation**: The retrieved context + the user's question are sent to `ChatOllama` (Llama 3) to generate a precise answer.

---
*Created by [Ritesh Bavaliya](https://github.com/riteshb040) as a personal project to explore RAG and Local LLMs.*

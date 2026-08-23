# 🤖 Agentic RAG for Software Engineering QA

An **Agentic Retrieval-Augmented Generation (RAG)** system for answering software engineering questions using technical documentation and open-source source code.

The system combines **LangGraph-based agentic routing, Qdrant retrieval, query rewriting, retrieval grading, reranking, web-search fallback, and Mistral 7B** to produce context-aware answers.

A **Streamlit frontend** provides a visual execution trace so users can see how the agent routes a question, retrieves repository context, evaluates retrieval quality, retries when necessary, and optionally uses web search.

---

## ✨ Features

- 🧭 **Agentic Query Routing**
  - Direct path for simple/general questions
  - Retrieval path for repository-related questions
  - Complex path for deeper investigation

- 🔎 **Retrieval-Augmented Generation**
  - Dense vector retrieval from Qdrant
  - Repository documentation and source-code retrieval
  - Embedding-based semantic search
  - BGE-based reranking

- 🎯 **Corrective Retrieval**
  - Retrieval relevance grading
  - Low-quality retrieval detection
  - Query rewriting
  - Retrieval retry

- 🌐 **Web Search Fallback**
  - Uses Tavily when repository retrieval is insufficient
  - Helps answer questions requiring information outside the indexed repository

- 🧠 **Local LLM**
  - Mistral 7B through Ollama

- ⚡ **FastAPI REST API**
  - Exposes the RAG pipeline through an HTTP API

- 🎨 **Streamlit Frontend**
  - Clean question-answering interface
  - Agent execution trace
  - Retrieval statistics
  - Retrieved source files
  - Query rewrite visibility
  - Web-search visibility
  - Developer/debug information

- 🐳 **Docker Support**
  - Dockerized FastAPI application
  - Docker Compose configuration for Qdrant

- 📊 **Evaluation**
  - Benchmark runner
  - Latency tracking
  - RAGAS evaluator for:
    - Answer Relevancy
    - Faithfulness
    - Context Precision

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │  Streamlit Frontend │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI REST API │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    RAG Pipeline     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangGraph Agent   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                  ┌─────────────┐       ┌─────────────┐
                  │ Query Router│       │ Direct Path │
                  └──────┬──────┘       └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Qdrant    │
                  │   Retrieval │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ BGE Reranker│
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Retrieval   │
                  │   Grader    │
                  └──────┬──────┘
                         │
                    Relevant?
                    /       \
                  Yes        No
                   │          │
                   │          ▼
                   │    ┌──────────────┐
                   │    │ Query Rewrite│
                   │    └──────┬───────┘
                   │           │
                   │           ▼
                   │     Re-retrieval
                   │
                   └──────┬────────────┘
                          │
                   Still insufficient?
                          │
                          ▼
                   ┌─────────────┐
                   │ Tavily Web  │
                   │   Search    │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Mistral 7B  │
                   │   Ollama    │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Final Answer│
                   └─────────────┘
```

---

# 🔄 Query Flow

For a repository-related question:

```text
User Question
      │
      ▼
Query Router
      │
      ▼
Repository Retrieval
      │
      ▼
Reranking
      │
      ▼
Retrieval Grader
      │
      ├── Relevant ──────────────► Answer Generation
      │
      └── Not Relevant
                │
                ▼
          Query Rewriting
                │
                ▼
           Re-retrieval
                │
                ├── Relevant ────► Answer Generation
                │
                └── Still weak
                        │
                        ▼
                  Tavily Web Search
                        │
                        ▼
                  Answer Generation
```

For a simple general question:

```text
User Question
      │
      ▼
Query Router
      │
      ▼
DIRECT
      │
      ▼
Answer Generation
```

---

# 🧩 Tech Stack

## LLM

- **Mistral 7B**
- **Ollama**

## Agent / RAG Framework

- **LangGraph**
- **LangChain**

## Backend

- **FastAPI**
- **Uvicorn**
- REST API

## Vector Retrieval

- **Qdrant**
- Sentence-transformer embeddings
- **BGE Cross-Encoder Reranker**

## Web Search

- **Tavily**

## Frontend

- **Streamlit**

## Code / Document Processing

- Repository indexing
- Documentation and source-code chunking
- AST-aware code processing

## Evaluation

- **RAGAS**
- Benchmark runner
- Latency measurement

## Infrastructure

- **Docker**
- **Docker Compose**

---

# 📁 Project Structure

```text
agentic-rag-se-qa/
│
├── app/
│   ├── agents/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── qdrant.py
│   ├── embeddings/
│   ├── evaluation/
│   │   ├── benchmark.py
│   │   └── ragas_evaluator.py
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── query_rewriter.py
│   │   ├── retrieval_grader.py
│   │   ├── router.py
│   │   ├── state.py
│   │   └── workflow.py
│   ├── ingestion/
│   ├── llm/
│   │   └── ollama_client.py
│   ├── models/
│   ├── prompts/
│   ├── rag/
│   │   └── rag_pipeline.py
│   ├── retrieval/
│   ├── services/
│   ├── vectorstore/
│   │   └── qdrant_client.py
│   ├── websearch/
│   │   └── web_searcher.py
│   ├── main.py
│   └── streamlit_app.py
│
├── data/
│   ├── benchmark.json
│   └── raw/
│       └── repos/
│
├── docker/
├── scripts/
│   └── index_repository.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ How the System Works

### 1. Repository Ingestion

Technical documentation and source code are collected from the target repository.

### 2. Chunking

The repository is split into useful chunks so that individual pieces of documentation and code can be retrieved.

### 3. Embeddings

Chunks are converted into vector representations using the configured embedding model.

### 4. Vector Storage

Embeddings and their associated content are stored in **Qdrant**.

### 5. Query Routing

The LangGraph router decides whether the question should:

- take the direct path, or
- use repository retrieval.

### 6. Retrieval

For retrieval-based questions, relevant repository chunks are retrieved from Qdrant.

### 7. Reranking

Retrieved candidates can be reranked using a BGE cross-encoder to improve relevance.

### 8. Retrieval Grading

The retrieval grader evaluates whether the retrieved context is useful for answering the question.

### 9. Query Rewriting

If retrieval quality is insufficient, the agent can rewrite the query and retry retrieval.

### 10. Web Search

If the available repository context is still insufficient, the system can use Tavily web search.

### 11. Answer Generation

The collected context is passed to **Mistral 7B through Ollama**, which generates the final answer.

---

# 🎨 Streamlit Frontend

The frontend is designed to make the agent's reasoning flow visible.

It displays:

```text
Question
   ↓
Query Router
   ↓
Vector Retrieval
   ↓
Retrieval Grader
   ↓
Query Rewrite / Retry
   ↓
Web Search (when needed)
   ↓
Final Answer
```

The interface also exposes:

- Selected route
- Number of retrieved documents
- Retrieval score
- Retry count
- Web-search usage
- Retrieved repository sources
- Optional retrieved context
- Rewritten query
- Web-search sources
- Developer/debug information

This makes it easier to demonstrate the system during development and technical interviews.

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/pavanbhatkar1/agentic-rag-se-qa.git
cd agentic-rag-se-qa
```

Create a virtual environment:

```bash
python -m venv .venv1
```

### Windows

```powershell
.\.venv1\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv1/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
QDRANT_COLLECTION=software_docs

QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

TAVILY_API_KEY=
```

> Do not commit `.env` or API keys to GitHub.

For a Dockerized FastAPI container connecting to Qdrant and a locally running Ollama instance, the container can use:

```text
QDRANT_URL=http://qdrant:6333
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

# 🗄️ Start Qdrant

The project includes a Docker Compose configuration for Qdrant.

```powershell
docker compose up -d qdrant
```

Check running containers:

```powershell
docker ps
```

Qdrant is exposed on:

```text
http://localhost:6333
```

---

# 📚 Index the Repository

Use the repository indexing script:

```powershell
python .\scripts\index_repository.py
```

The indexed documents are stored in the configured Qdrant collection.

---

# ⚡ Run FastAPI

Run the backend locally:

```powershell
python -m uvicorn app.main:app --reload --port 10000
```

API:

```text
http://localhost:10000
```

Swagger documentation:

```text
http://localhost:10000/docs
```

---

# 🎨 Run Streamlit

From the project root:

```powershell
python -m streamlit run .\app\streamlit_app.py --server.port 8502
```

Open:

```text
http://localhost:8502
```

---

# 🐳 Run with Docker

Build the application image:

```powershell
docker build -t agentic-rag .
```

The FastAPI container needs access to Qdrant and Ollama.

Example:

```powershell
docker run --rm `
  --network agentic-rag-se-qa_default `
  -p 10000:8000 `
  --env-file .env `
  -e QDRANT_URL=http://qdrant:6333 `
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
  agentic-rag
```

The Dockerized API is then available at:

```text
http://localhost:10000
```

---

# 🔌 API

The main API exposes the RAG pipeline through a query endpoint.

### POST `/query`

Example:

```json
{
  "question": "How does FastAPI define an API route?"
}
```

Example response structure:

```json
{
  "answer": "FastAPI defines routes using path operation decorators...",
  "route": "retrieve",
  "retrieval_score": 1.0,
  "web_search_used": false,
  "retry_count": 0
}
```

---

# 📊 Evaluation

The project contains two evaluation components:

```text
app/evaluation/
├── benchmark.py
└── ragas_evaluator.py
```

### Benchmark

The benchmark runner records:

- Question
- Ground truth
- Generated answer
- Retrieved contexts
- Latency
- Route
- Retrieval score
- Retry count
- Web-search usage

Results are written to:

```text
data/benchmark_results.json
```

### RAGAS

The RAGAS evaluator currently uses:

- **Answer Relevancy**
- **Faithfulness**
- **Context Precision**

The benchmark dataset and evaluation setup are intentionally kept as-is for now and can be updated with finalized benchmark results later.

---

# 📈 Results

> **Benchmark results will be updated after the current benchmark run is finalized.**

Current evaluation results are intentionally not listed here yet.

The project is set up to report:

| Metric | Result |
|---|---:|
| Answer Relevancy | TBD |
| Faithfulness | TBD |
| Context Precision | TBD |
| Average Latency | TBD |

---

# 🧪 Example Questions

### Repository Retrieval

```text
How does FastAPI define an API route?
```

Expected behavior:

```text
Router
  ↓
Retrieve
  ↓
Qdrant
  ↓
Retrieval Grader
  ↓
Mistral
```

### Direct Question

```text
What is 2 + 2?
```

Expected behavior:

```text
Router
  ↓
Direct
  ↓
Mistral
```

### Difficult / Insufficient Retrieval

A question that cannot be sufficiently answered from the indexed repository can trigger:

```text
Retrieve
   ↓
Low relevance
   ↓
Query Rewrite
   ↓
Retry
   ↓
Web Search
   ↓
Answer
```

---

# 🧠 Why Agentic RAG?

A traditional RAG pipeline generally follows:

```text
Question
   ↓
Retrieve
   ↓
Generate
```

This project adds decision-making around retrieval:

```text
Question
   ↓
Should retrieval be used?
   ↓
Retrieve
   ↓
Is the context relevant?
   ↓
No ──► Rewrite ──► Retry
                 ↓
             Still weak?
                 ↓
             Web Search
                 ↓
              Generate
```

This allows the system to adapt its retrieval strategy instead of blindly generating an answer from the first retrieved documents.

---

# 🎯 Resume Highlights

- Developed an **Agentic RAG system for software engineering question answering** over technical documentation and open-source code repositories.
- Implemented **LangGraph-based query routing, retrieval grading, query rewriting, and retry workflows**.
- Integrated **Qdrant vector search, embedding-based retrieval, and BGE reranking** for repository-level context retrieval.
- Added **Tavily web-search fallback** when repository context is insufficient.
- Integrated **Mistral 7B through Ollama** for local answer generation.
- Built a **FastAPI REST API** and **Streamlit frontend** for interactive question answering and agent execution visualization.
- Containerized the backend using **Docker** and configured Qdrant using Docker Compose.
- Implemented benchmark and **RAGAS evaluation** for answer relevancy, faithfulness, context precision, and latency.

---

# 🔮 Future Improvements

- Finalize and expand benchmark evaluation
- Multi-repository indexing
- Streaming responses
- GitHub repository integration
- Incremental repository indexing
- Support for additional LLMs
- Improved observability and tracing
- Production cloud deployment

---

# 📄 License

This project is intended for educational and research purposes.

# AI Career Assistant

![CI](https://github.com/tiagorcfortunato/ai-career-assistant/actions/workflows/ci.yml/badge.svg)

A production-deployed **Retrieval-Augmented Generation (RAG)** career chatbot. Recruiters and hiring managers can ask natural-language questions about Tiago Fortunato's experience, projects, and skills, and receive accurate, sourced answers in real time with streaming responses.

> **Live demo:** [https://chatbot.tifortunato.com](https://chatbot.tifortunato.com)

---

## Features

- **Hybrid retrieval** — combines semantic search (ChromaDB embeddings) with keyword search (BM25), fused via Reciprocal Rank Fusion (RRF) for best-of-both-worlds matching
- **Streaming SSE responses** — token-by-token output via Server-Sent Events for a ChatGPT-like experience
- **Section-aware chunking** — for PDFs, detects headings by font-size analysis (PyMuPDF); for Markdown, splits by ATX headings
- **Conversation history** — follow-up questions resolve references via short-query history enrichment
- **Source attribution** — every answer shows which sections informed the response
- **RAGAS evaluation pipeline** — automated quality metrics (faithfulness, relevancy, context precision/recall) using Gemini as judge
- **Pre-build knowledge ingestion** — vector store baked into Docker image to avoid runtime memory spikes
- **Production deployment** — AWS EC2 + Docker + Nginx + Let's Encrypt HTTPS + custom domain

---

## Architecture

```
Knowledge base (Markdown)
    ↓
Section-aware chunking (ATX headings)
    ↓
Local embeddings (BAAI/bge-small-en-v1.5 via fastembed)
    ↓
ChromaDB (persistent, pre-ingested at Docker build time)

─────────────────────────────────────────

User question
    ↓
History enrichment for short queries
    ↓
Hybrid search:
  ├── Semantic search (ChromaDB top-k)
  └── BM25 keyword search (top-k)
       ↓
Reciprocal Rank Fusion → top chunks
    ↓
LangChain prompt: system + history + context + question
    ↓
Groq LLM (llama-3.1-8b-instant, temperature=0)
    ↓
Streaming SSE tokens → frontend
```

---

## Tech stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI |
| **LLM** | Llama 3.1 8B Instant via [Groq](https://groq.com) |
| **Embeddings** | `BAAI/bge-small-en-v1.5` (fastembed, runs locally) |
| **Vector DB** | ChromaDB (persistent) |
| **Keyword search** | BM25 via `rank_bm25` |
| **Orchestration** | LangChain |
| **Streaming** | Server-Sent Events (SSE) |
| **Frontend** | Vanilla HTML/CSS/JS + marked.js |
| **Evaluation** | RAGAS with Gemini 2.5 Flash as judge |
| **Deployment** | Docker, AWS EC2, Nginx, Let's Encrypt |
| **CI/CD** | GitHub Actions |

---

## Getting started

### Prerequisites

- Docker and Docker Compose
- A free [Groq API key](https://console.groq.com)

### Setup

```bash
git clone https://github.com/tiagorcfortunato/ai-career-assistant.git
cd ai-career-assistant

cp .env.example .env
# Edit .env and set your GROQ_API_KEY
```

### Run

```bash
docker-compose up --build
```

- **Chat UI:** `http://localhost:8000`
- **API docs:** `http://localhost:8000/docs`

The first build downloads the embedding model (~80MB) and pre-ingests the knowledge base. Subsequent starts are instant.

---

## API reference

### Query (non-streaming)

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What projects has Tiago built?",
    "history": []
  }'
```

```json
{
  "answer": "Tiago has built three main projects...",
  "sources": [
    {
      "content": "chunk preview...",
      "page": 1,
      "section": "Projects Overview",
      "document_id": "..."
    }
  ]
}
```

### Query (streaming SSE)

```bash
curl -N -X POST http://localhost:8000/api/query/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about yourself", "history": []}'
```

Response is a stream of SSE events:

```
data: {"sources": [...]}

data: {"token": "Tiago"}
data: {"token": " is"}
...
data: [DONE]
```

### Upload a PDF

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"
```

---

## Project structure

```
app/
├── api/
│   └── routes.py              # Upload, query, stream endpoints
├── services/
│   ├── ingestion.py           # PDF/MD → section-aware chunks → ChromaDB
│   ├── retrieval.py           # Hybrid search (semantic + BM25 + RRF) → LLM
│   └── embeddings.py          # FastEmbeddings wrapper
├── models/
│   └── schemas.py             # Pydantic request/response models
├── static/
│   └── index.html             # Chat UI with markdown rendering
├── config.py                  # Pydantic settings from env
└── main.py                    # FastAPI app + lifespan startup

data/
└── knowledge_base.md          # Career knowledge base (pre-ingested)

tests/                         # Pytest tests for upload, query, health
eval_ragas.py                  # RAGAS evaluation pipeline
Dockerfile                     # Pre-ingests KB at build time
```

---

## Evaluation

Run RAGAS evaluation against the live deployment:

```bash
GOOGLE_API_KEY=your_gemini_key python eval_ragas.py
```

Metrics evaluated:
- **Faithfulness** — Are factual claims grounded in retrieved context?
- **Answer Relevancy** — Does the answer address the question?
- **Context Precision** — Are retrieved chunks relevant?
- **Context Recall** — Were the right chunks retrieved?

Gemini 2.5 Flash is used as the evaluator LLM (different from the chatbot's Groq model — best practice for unbiased evaluation).

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | required | Your Groq API key (free at console.groq.com) |
| `LLM_MODEL` | `llama-3.1-8b-instant` | Groq model to use |
| `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | Local embedding model |
| `CHROMA_PATH` | `./chroma_db` | ChromaDB persistence directory |
| `CHUNK_SIZE` | `500` | Max characters per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `RETRIEVAL_K` | `8` | Number of chunks retrieved per query |
| `GOOGLE_API_KEY` | optional | For RAGAS evaluation only |

---

## Production deployment

The live demo runs on AWS EC2 (t3.micro) with:
- Docker container managed via `--restart unless-stopped`
- Nginx reverse proxy on ports 80/443
- Let's Encrypt SSL certificate with auto-renewal cron
- Custom domain via Namecheap DNS A record
- Pre-build knowledge base ingestion (avoids runtime OOM on 1GB RAM)
- Swap space for safer Docker builds

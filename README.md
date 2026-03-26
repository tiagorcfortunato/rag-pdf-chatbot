# RAG PDF Chatbot

A production-ready Retrieval-Augmented Generation (RAG) API that lets you upload PDFs and ask questions about their content.

Built with **LangChain**, **Claude (Anthropic)**, **ChromaDB**, and **FastAPI**. Fully containerized with Docker.

## How it works

```
PDF upload → text extraction → chunking → embeddings (local) → ChromaDB
                                                                    ↓
Question → embed question → similarity search → top-K chunks → Claude → Answer
```

1. **Ingest**: PDF is split into overlapping chunks (~500 tokens each), embedded using a local Sentence Transformers model, and stored in ChromaDB.
2. **Query**: The question is embedded and compared against all stored chunks. The top-4 most relevant chunks are retrieved and passed as context to Claude, which generates a grounded answer.

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| LLM | Claude 3.5 Haiku (Anthropic) |
| Embeddings | `all-MiniLM-L6-v2` (Sentence Transformers, runs locally) |
| Vector DB | ChromaDB (persistent, local) |
| Framework | LangChain |
| Deployment | Docker / Docker Compose |

## Getting started

### Prerequisites

- Docker and Docker Compose
- An [Anthropic API key](https://console.anthropic.com)

### Setup

```bash
git clone https://github.com/tiagorcfortunato/rag-pdf-chatbot.git
cd rag-pdf-chatbot

cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

Interactive docs at `http://localhost:8000/docs`.

## API

### Upload a PDF

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@your-document.pdf"
```

```json
{
  "document_id": "a1b2c3d4-...",
  "filename": "your-document.pdf",
  "chunks_count": 42
}
```

### Ask a question

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the document?", "document_id": "a1b2c3d4-..."}'
```

```json
{
  "answer": "The document is about ...",
  "sources": [
    {
      "content": "Relevant chunk preview...",
      "page": 3,
      "document_id": "a1b2c3d4-..."
    }
  ]
}
```

### List uploaded documents

```bash
curl http://localhost:8000/api/documents
```

## Project structure

```
app/
├── api/
│   └── routes.py        # API endpoints
├── services/
│   ├── ingestion.py     # PDF → chunks → ChromaDB
│   └── retrieval.py     # question → search → Claude → answer
├── models/
│   └── schemas.py       # Pydantic request/response models
├── config.py            # Settings from .env
└── main.py              # FastAPI app
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | required | Your Anthropic API key |
| `CLAUDE_MODEL` | `claude-3-5-haiku-20241022` | Claude model to use |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence Transformers model |
| `CHUNK_SIZE` | `500` | Tokens per chunk |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `RETRIEVAL_K` | `4` | Number of chunks retrieved per query |

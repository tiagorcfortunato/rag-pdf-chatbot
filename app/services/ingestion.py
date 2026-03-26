import uuid
from pathlib import Path

import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import settings


def _get_vector_store() -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=embeddings,
    )


def ingest_pdf(file_path: Path, filename: str) -> tuple[str, int]:
    """
    Reads a PDF, splits into chunks, embeds and stores in ChromaDB.
    Returns (document_id, chunks_count).
    """
    document_id = str(uuid.uuid4())

    # 1. Extract text from PDF
    raw_pages = _extract_pages(file_path)

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    chunks = []
    metadatas = []
    for page_num, text in raw_pages:
        page_chunks = splitter.split_text(text)
        for chunk in page_chunks:
            chunks.append(chunk)
            metadatas.append({
                "document_id": document_id,
                "filename": filename,
                "page": page_num,
            })

    # 3. Store in ChromaDB
    vector_store = _get_vector_store()
    vector_store.add_texts(texts=chunks, metadatas=metadatas)

    return document_id, len(chunks)


def _extract_pages(file_path: Path) -> list[tuple[int, str]]:
    """Returns list of (page_number, text) for each page."""
    pages = []
    with fitz.open(str(file_path)) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if text.strip():
                pages.append((page_num, text))
    return pages

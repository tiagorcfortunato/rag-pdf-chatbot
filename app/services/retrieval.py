from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from app.services.embeddings import FastEmbeddings
from langchain.prompts import ChatPromptTemplate

from app.config import settings
from app.models.schemas import QueryResponse, Source


PROMPT_TEMPLATE = """You are an assistant that answers questions based strictly on the provided context.
If the answer is not in the context, say "I couldn't find that information in the provided document."
Do not make up information.

Context:
{context}

Question: {question}

Answer:"""


def _get_vector_store() -> Chroma:
    embeddings = FastEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        persist_directory=settings.chroma_path,
        embedding_function=embeddings,
    )


def query(question: str, document_id: str | None = None) -> QueryResponse:
    """
    Searches ChromaDB for relevant chunks, then asks Claude to answer.
    """
    vector_store = _get_vector_store()

    # 1. Build search filter (optional: restrict to one document)
    search_filter = {"document_id": document_id} if document_id else None

    # 2. Similarity search — returns top-K most relevant chunks
    results = vector_store.similarity_search(
        query=question,
        k=settings.retrieval_k,
        filter=search_filter,
    )

    if not results:
        return QueryResponse(
            answer="I couldn't find any relevant information in the uploaded documents.",
            sources=[],
        )

    # 3. Build context string from retrieved chunks
    context = "\n\n---\n\n".join([doc.page_content for doc in results])

    # 4. Assemble prompt and call Claude
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
    )
    chain = prompt | llm

    response = chain.invoke({"context": context, "question": question})

    # 5. Build sources list for the response
    sources = [
        Source(
            content=doc.page_content[:200],  # preview of the chunk
            page=doc.metadata.get("page", 0),
            document_id=doc.metadata.get("document_id", ""),
        )
        for doc in results
    ]

    return QueryResponse(answer=response.content, sources=sources)

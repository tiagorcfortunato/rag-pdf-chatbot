from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings


class FastEmbeddings(Embeddings):
    """Thin wrapper around fastembed that implements the LangChain Embeddings interface."""

    def __init__(self, model_name: str):
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [embedding.tolist() for embedding in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return list(self._model.embed([text]))[0].tolist()

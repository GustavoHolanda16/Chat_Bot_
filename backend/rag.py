from embeddings import EmbeddingService
from vectorstore import VectorStore
from database import SessionLocal
from models import Produto
import numpy as np

class RAGipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vectors = VectorStore()

    def prepare(self):
        db = SessionLocal()
        produtos = db.query(Produto).all()

        textos = [p.descricao for p in produtos]
        embeddings = self.embedder.encode(textos)

        self.vectors.add(embeddings)
        self.vectors.save()

        return len(produtos)

    def retrive(self, query):
        q_emb = self.embedder.encode([query])
        indices = self.vectors.search(q_emb, k=5)

        db = SessionLocal()
        produtos = db.query(Produto).all()

        return [produtos[i] for i in indices]
    
     
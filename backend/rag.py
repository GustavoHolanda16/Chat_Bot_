# rag.py - CORRIGIDO
from embeddings import EmbeddingService
from vectorstore import VectorStore
from database import SessionLocal
from models import Produto
import numpy as np

class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vectors = VectorStore()
        self.produto_ids = []
        self.produtos_cache = {}  # Cache para acesso rápido

    def prepare(self):
        db = SessionLocal()
        try:
            produtos = db.query(Produto).all()
            
            if not produtos:
                raise Exception("Nenhum produto encontrado no banco de dados")
            
            # Cache de produtos para acesso rápido
            self.produtos_cache = {p.id: p for p in produtos}
            self.produto_ids = [p.id for p in produtos]
            
            textos = [self._criar_texto_indexacao(p) for p in produtos]
            embeddings = self.embedder.encode(textos)

            self.vectors.add(embeddings)
            self.vectors.save()

            print(f"Pipeline preparado com {len(produtos)} produtos")
            return len(produtos)
        finally:
            db.close()

    def _criar_texto_indexacao(self, produto: Produto) -> str:
        """Cria texto otimizado para busca"""
        return f"{produto.tipo} {produto.variante} {produto.manga} {produto.cor} {produto.descricao}".lower()

    def retrieve(self, query, k=5):  
        if not self.produto_ids:
            raise Exception("Pipeline não preparado. Execute prepare() primeiro.")
        
        # Limpa e normaliza a query
        query_clean = query.lower().strip()
        q_emb = self.embedder.encode([query_clean])
        
        # Busca mais resultados para filtrar depois
        indices = self.vectors.search(q_emb, k=min(k + 5, len(self.produto_ids)))
        
        # Filtra índices válidos
        indices_validos = [i for i in indices if i < len(self.produto_ids)]
        
        if not indices_validos:
            print("Nenhum produto relevante encontrado")
            return []
        
        # Recupera produtos do cache
        produtos_encontrados = []
        for idx in indices_validos[:k]:  # Limita aos k melhores
            produto_id = self.produto_ids[idx]
            if produto_id in self.produtos_cache:
                produtos_encontrados.append(self.produtos_cache[produto_id])
        
        print(f"Retrieved {len(produtos_encontrados)} produtos para query: '{query}'")
        return produtos_encontrados
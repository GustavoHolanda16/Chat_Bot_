# rag.py - CORRIGIDO
from embeddings import EmbeddingService
from vectorstore import VectorStore
from database import SessionLocal
from models import Produto
import numpy as np
import logging
import re
from typing import List

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vectors = VectorStore(dimension=384)
        self.produto_ids = []
        self.produtos_cache = {}
        self.tipos_produtos = set()

    def prepare(self):
        db = SessionLocal()
        try:
            produtos = db.query(Produto).all()
            
            if not produtos:
                raise Exception("Nenhum produto encontrado no banco de dados")
            
            self.produtos_cache = {p.id: p for p in produtos}
            self.produto_ids = [p.id for p in produtos]
            self.tipos_produtos = {p.tipo.lower() for p in produtos}
            
            textos = [self._criar_texto_indexacao(p) for p in produtos]
            logger.info(f"Gerando embeddings para {len(textos)} produtos...")
            
            embeddings = self.embedder.encode(textos)
            self.vectors.add(embeddings)
            self.vectors.save()

            logger.info(f"Pipeline preparado com {len(produtos)} produtos")
            logger.info(f"Tipos disponíveis: {self.tipos_produtos}")
            return len(produtos)
        except Exception as e:
            logger.error(f"Erro no prepare: {e}")
            raise
        finally:
            db.close()

    def _criar_texto_indexacao(self, produto: Produto) -> str:
        """Cria texto rico para indexação"""
        texto = f"""
        camisa {produto.tipo} {produto.variante} manga {produto.manga} 
        cor {produto.cor} {produto.descricao}
        preço {produto.preco} estoque {produto.estoque}
        """.lower()
        return re.sub(r'\s+', ' ', texto).strip()

    def retrieve(self, query, k=8):
        if not self.produto_ids:
            raise Exception("Pipeline não preparado. Execute prepare() primeiro.")
        
        # CORREÇÃO: Use o método público de normalização
        query_clean = self._normalizar_query(query)
        logger.info(f"Buscando produtos para: '{query_clean}'")
        
        # Estratégia 1: Busca semântica com embeddings
        produtos_semanticos = self._busca_semantica(query_clean, k)
        
        # Estratégia 2: Busca por palavra-chave
        produtos_keywords = self._busca_por_palavra_chave(query_clean, k)
        
        # Estratégia 3: Busca por sinônimos e correções
        produtos_sinonimos = self._busca_por_sinonimos(query_clean, k)
        
        # Combina resultados eliminando duplicatas
        todos_produtos = produtos_semanticos + produtos_keywords + produtos_sinonimos
        
        # Remove duplicatas mantendo ordem
        produtos_unicos = []
        ids_vistos = set()
        for produto in todos_produtos:
            if produto.id not in ids_vistos:
                produtos_unicos.append(produto)
                ids_vistos.add(produto.id)
        
        # Limita ao número máximo de resultados
        resultados_finais = produtos_unicos[:k]
        
        logger.info(f"Encontrados {len(resultados_finais)} produtos para: '{query}'")
        return resultados_finais

    def _normalizar_query(self, query: str) -> str:
        """Normaliza a query usando o mesmo método do embedder"""
        # Reimplementa a normalização aqui para evitar o erro
        if not query:
            return ""
        
        query = query.lower()
        
        # Correções básicas
        correcoes = {
            'camsia': 'camisa', 'camiza': 'camisa',
            'pollo': 'polo', 'socia': 'social',
            'casua': 'casual', 'premiu': 'premium',
            'cores': 'cor', 'valor': 'preço'
        }
        
        for erro, correcao in correcoes.items():
            query = query.replace(erro, correcao)
        
        query = re.sub(r'[^\w\s]', ' ', query)
        query = re.sub(r'\s+', ' ', query).strip()
        
        return query

    def _busca_semantica(self, query: str, k: int) -> List[Produto]:
        """Busca usando embeddings semânticos"""
        try:
            q_emb = self.embedder.encode([query])
            indices = self.vectors.search(q_emb, k=k*2)
            
            produtos = []
            for idx in indices:
                if idx < len(self.produto_ids):
                    produto_id = self.produto_ids[idx]
                    if produto_id in self.produtos_cache:
                        produtos.append(self.produtos_cache[produto_id])
            
            return produtos
        except Exception as e:
            logger.error(f"Erro na busca semântica: {e}")
            return []

    def _busca_por_palavra_chave(self, query: str, k: int) -> List[Produto]:
        """Busca por palavras-chave com pesos"""
        palavras = query.split()
        produtos_com_peso = []
        
        for produto in self.produtos_cache.values():
            peso = 0
            texto_produto = self._criar_texto_indexacao(produto).lower()
            
            for palavra in palavras:
                if palavra in texto_produto:
                    # Dá pesos diferentes baseado na importância
                    if palavra in ['polo', 'social', 'casual', 'esportiva', 'premium']:
                        peso += 3
                    elif palavra in ['azul', 'vermelho', 'preto', 'branco', 'verde', 'amarelo', 'roxo', 'cinza', 'bege', 'vinho', 'rosa', 'laranja']:
                        peso += 2
                    elif palavra in ['manga', 'curta', 'longa']:
                        peso += 2
                    elif palavra in ['estampada', 'básica', 'lisa']:
                        peso += 1
                    else:
                        peso += 1
            
            if peso > 0:
                produtos_com_peso.append((peso, produto))
        
        produtos_com_peso.sort(key=lambda x: x[0], reverse=True)
        return [produto for peso, produto in produtos_com_peso[:k]]

    def _busca_por_sinonimos(self, query: str, k: int) -> List[Produto]:
        """Busca usando sinônimos e correções"""
        sinônimos = {
            'social': ['social', 'formal', 'trabalho'],
            'polo': ['polo', 'esporte', 'esportiva'],
            'casual': ['casual', 'basica', 'básica'],
            'premium': ['premium', 'luxo'],
            'esportiva': ['esportiva', 'dry-fit']
        }
        
        palavras_expandidas = []
        for palavra in query.split():
            if palavra in sinônimos:
                palavras_expandidas.extend(sinônimos[palavra])
            else:
                palavras_expandidas.append(palavra)
        
        query_expandida = ' '.join(palavras_expandidas)
        return self._busca_por_palavra_chave(query_expandida, k)
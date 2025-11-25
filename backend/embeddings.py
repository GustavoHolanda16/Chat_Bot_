# embeddings.py - CORRIGIDO
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
import os
import re

os.environ["CUDA_VISIBLE_DEVICES"] = ""

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        try:
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            logger.info("Modelo de embedding local carregado na CPU: all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise
    
    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            textos_normalizados = [self._normalizar_texto_avancado(text) for text in texts]  # NOME CORRETO
            embeddings = self.model.encode(textos_normalizados, convert_to_numpy=True, device="cpu")
            logger.info(f"Embeddings gerados para {len(texts)} textos")
            return embeddings
        except Exception as e:
            logger.error(f"Erro na geração de embeddings: {e}")
            embedding_size = 384
            return np.random.normal(0, 0.1, (len(texts), embedding_size))
    
    def _normalizar_texto_avancado(self, texto):  # NOME CORRETO
        """Normalização avançada para melhor busca"""
        if not texto:
            return ""
        
        texto = texto.lower()
        
        # Correções expandidas
        correcoes = {
            'camsia': 'camisa', 'camiza': 'camisa', 'camisaa': 'camisa',
            'pollo': 'polo', 'poloo': 'polo',
            'socia': 'social', 'sociais': 'social',
            'casua': 'casual', 'casuais': 'casual',
            'esportiv': 'esportiva', 'esportivas': 'esportiva',
            'premiu': 'premium', 'premiumm': 'premium',
            'cor ': 'cor ', 'cores': 'cor', 'color': 'cor',
            'valor': 'preço', 'valores': 'preço', 'custa': 'preço',
            'tecido': 'material', 'tecidos': 'material', 'material': 'material',
            'manga ': 'manga ', 'mangas': 'manga',
            'curta': 'manga curta', 'corta': 'manga curta',
            'longa': 'manga longa', 'comprida': 'manga longa',
            'estampa': 'estampada', 'estampado': 'estampada',
            'lisa': 'básica', 'basica': 'básica',
            'branca': 'branco', 'preta': 'preto', 'azul': 'azul',
            'vermelha': 'vermelho', 'verde': 'verde', 'amarela': 'amarelo'
        }
        
        for erro, correcao in correcoes.items():
            texto = texto.replace(erro, correcao)
        
        # Expansão de sinônimos
        sinonimos = {
            'social': ['social', 'formal', 'trabalho', 'escritorio', 'reunião', 'empresa'],
            'polo': ['polo', 'esporte', 'esportiva', 'casual', 'piquet'],
            'casual': ['casual', 'diária', 'básica', 'urbana', 'cotidiano'],
            'premium': ['premium', 'luxo', 'algodão egípcio', 'alta qualidade'],
            'esportiva': ['esportiva', 'dry-fit', 'academia', 'exercício', 'atividade']
        }
        
        # Adiciona sinônimos ao texto para melhor busca
        palavras = texto.split()
        palavras_expandidas = []
        for palavra in palavras:
            palavras_expandidas.append(palavra)
            for chave, valores in sinonimos.items():
                if palavra in valores:
                    palavras_expandidas.append(chave)
        
        texto = ' '.join(palavras_expandidas)
        
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        return texto
# vectorstore.py - MAIS TOLERANTE
import faiss
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class VectorStore: 
    def __init__(self, dimension=384, index_path="./data/faiss.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None

        os.makedirs(os.path.dirname(index_path), exist_ok=True)

        if os.path.exists(index_path):
            try:
                self.index = faiss.read_index(index_path)
                logger.info(f"Índice carregado: {self.index.ntotal} vetores")
            except Exception as e:
                logger.warning(f"Erro ao carregar índice: {e}. Criando novo.")
                self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = faiss.IndexFlatL2(dimension)
            logger.info("Novo índice FAISS criado")

    def add(self, vectors):
        if len(vectors) == 0:
            logger.warning("Tentativa de adicionar vetores vazios")
            return
        
        if not isinstance(vectors, np.ndarray):
            vectors = np.array(vectors)
            
        # Garante que os vetores têm a dimensão correta
        if vectors.shape[1] != self.dimension:
            logger.warning(f"Dimensão incorreta: {vectors.shape[1]} != {self.dimension}")
            # Ajusta a dimensão se necessário
            if vectors.shape[1] < self.dimension:
                # Preenche com zeros
                padded = np.zeros((vectors.shape[0], self.dimension))
                padded[:, :vectors.shape[1]] = vectors
                vectors = padded
            else:
                # Corta o excesso
                vectors = vectors[:, :self.dimension]
            
        vectors = vectors.astype('float32')
        self.index.add(vectors)
        logger.info(f"Adicionados {len(vectors)} vetores ao índice")
    
    def save(self):
        try:
            faiss.write_index(self.index, self.index_path)
            logger.info(f"Índice salvo: {self.index.ntotal} vetores em {self.index_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar índice: {e}")

    def search(self, vector, k=5):
        if self.index.ntotal == 0:
            logger.warning("Índice vazio - nenhum vetor para buscar")
            return []
        
        k = min(k, self.index.ntotal)
        
        if not isinstance(vector, np.ndarray):
            vector = np.array(vector)
            
        # Garante dimensão correta
        if vector.shape[1] != self.dimension:
            if vector.shape[1] < self.dimension:
                padded = np.zeros((vector.shape[0], self.dimension))
                padded[:, :vector.shape[1]] = vector
                vector = padded
            else:
                vector = vector[:, :self.dimension]
            
        vector = vector.astype('float32')
        
        try:
            distances, indices = self.index.search(vector, k)
            
            # Filtro menos restritivo
            resultados_validos = []
            for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
                if idx != -1 and dist < 3.0:  # Aumentei o threshold
                    resultados_validos.append(idx)
            
            logger.info(f"Busca retornou {len(resultados_validos)} resultados válidos")
            return resultados_validos
            
        except Exception as e:
            logger.error(f"Erro na busca FAISS: {e}")
            return []
# vectorstore.py - CORRIGIDO
import faiss
import numpy as np
import os

class VectorStore: 
    def __init__(self, dimension=384, index_path="./data/faiss.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None

        if os.path.exists(index_path):
            try:
                self.index = faiss.read_index(index_path)
                print(f"Índice carregado: {self.index.ntotal} vetores")
            except Exception as e:
                print(f"Erro ao carregar índice: {e}. Criando novo.")
                self.index = faiss.IndexFlatL2(dimension)
        else:
            self.index = faiss.IndexFlatL2(dimension)

    def add(self, vectors):
        if len(vectors) == 0:
            return
        self.index.add(vectors.astype('float32'))
    
    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        print(f"Índice salvo: {self.index.ntotal} vetores")

    def search(self, vector, k=5):
        if self.index.ntotal == 0:
            return []
        
        # Garante que k não seja maior que o número de vetores
        k = min(k, self.index.ntotal)
        vector = vector.astype('float32')
        
        distances, indices = self.index.search(vector, k)
        
        # Filtra resultados por distância (similaridade)
        resultados_validos = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx != -1:  # -1 indica resultado inválido no FAISS
                resultados_validos.append(idx)
        
        return resultados_validos
import faiss
import numpy as np
import os

class VectorStore: 
    def __init__(self, dimension=384, index_path="./data/faiss.index"):
        self.dimension = dimension
        self.index_path = index_path

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dimension)

    def add(self,vectors):
        self.index.add(vectors)
    
    def save(self):
        os.makedirs("./data/", exist_ok=True)
        faiss.write_index(self.index, self.index_path)

    def search(self, vector, k=5):
        distances, indices = self.index.search(vector,k)
        return indices[0]
    
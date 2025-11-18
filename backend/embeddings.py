from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6.V2")
    
    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

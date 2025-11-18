import requests
import json

class OllamaClient:
    def __init__ (self, model="llama3.2"):
        self.model = model

    def generate(self, prompt):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":self.model,"prompt":prompt, "stream":False}
        )

        return response.json()["response"]
    
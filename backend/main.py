from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from populate import popular
from rag import RAGipeline
from ollama_client import OllamaClient

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGipeline()
llm = OllamaClient()

@app.post("/prepare-db")
def prepare_db():
    popular()
    total = rag.prepare()
    return {"status":"ok","produtos":total}

@app.get("/chat")
async def chat(q:str):
    docs = rag.retrive(q)
    contexto = "\n".join([f"- {d.descricao}" for d in docs])

    prompt = f""" 
Você é um assistente de vendas de uma loja de camisas. 
Use SOMENTE os dados fornecidos abaixo:

{contexto}

Pergunta: {q}
"""
    resposta = llm.generate(prompt)

    async def event_gen():
        yield{"data": resposta}

    return EventSourceResponse(event_gen())
# main.py - ATUALIZADO PARA GEMINI
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from populate import popular
from rag import RAGPipeline
from gemini_client import GeminiClient  # Alterado aqui
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Consulta de Camisas - Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SISTEMA DO AGENTE
rag = None
agente = None
sistema_pronto = False

@app.on_event("startup")
async def startup_event():
    """Inicialização na startup"""
    global rag, agente
    try:
        rag = RAGPipeline()
        agente = GeminiClient()  # Alterado aqui
        logger.info("Sistema do agente Gemini inicializado")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")

@app.post("/prepare-db")
def preparar_sistema():
    try:
        global sistema_pronto, rag
        
        if rag is None:
            rag = RAGPipeline()
            
        logger.info("Preparando base de dados...")
        popular()
        total = rag.prepare()
        sistema_pronto = True
        logger.info(f"Sistema pronto com {total} produtos")
        return {"status": "ok", "produtos": total}
        
    except Exception as e:
        logger.error(f"Erro na preparação: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat")
async def chat(q: str = Query(..., min_length=1, description="Consulta do usuário")):
    start_time = time.time()
    
    try:
        global sistema_pronto, rag, agente
        
        logger.info(f"Consulta recebida: '{q}'")
        
        if not sistema_pronto or rag is None:
            return {
                "resposta": " Sistema em inicialização. Por favor, execute /prepare-db primeiro.",
                "produtos_encontrados": 0
            }
        
        # Busca produtos relevantes
        produtos = rag.retrieve(q, k=8)  # Aumentei para 8 produtos
        
        # Gera resposta profissional
        if agente is None:
            agente = GeminiClient()
            
        resposta = agente.generate(produtos, q)  # Passa a query original
        
        processing_time = time.time() - start_time
        logger.info(f"Consulta processada em {processing_time:.2f}s")
        
        return {
            "resposta": resposta, 
            "produtos_encontrados": len(produtos),
            "tempo_processamento": f"{processing_time:.2f}s"
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento da consulta: {e}")
        return {
            "resposta": " Desculpe, ocorreu um erro interno. Tente novamente.",
            "produtos_encontrados": 0
        }

@app.get("/health")
def verificar_saude():
    status = "operacional" if sistema_pronto else "inicializando"
    return {
        "status": status,
        "sistema_pronto": sistema_pronto,
        "rag_carregado": rag is not None,
        "agente_carregado": agente is not None
    }
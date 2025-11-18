# ollama_client.py - CORRIGIDO
import requests
import json
import os

class OllamaClient:
    def __init__(self, model="llama2", base_url=None):  # Modelo mais capaz
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")

    def generate(self, produtos: list) -> str:
        """
        Agente preciso: apenas descreve produtos reais do RAG
        """
        try:
            print(f"Agente: processando {len(produtos)} produtos")
            
            # Sempre usar resposta direta para garantir precisão
            if len(produtos) <= 3:
                return self._resposta_direta(produtos)
            
            # Para mais produtos, tentar LLM com controle rigoroso
            prompt = self._criar_prompt_rigoroso(produtos)
            resposta = self._chamar_ollama_controlado(prompt)
            
            return self._validar_resposta_rigorosa(resposta, produtos)
            
        except Exception as e:
            print(f"Agente falhou: {e}")
            # Fallback 100% preciso
            return self._resposta_direta(produtos)

    def _criar_prompt_rigoroso(self, produtos: list) -> str:
        """Prompt ultra-restritivo que força fidelidade aos dados"""
        
        produtos_texto = ""
        for i, produto in enumerate(produtos[:4], 1):
            produtos_texto += f"{i}. {produto.descricao} - Preço: R$ {produto.preco:.2f}\n"
        
        return f"""DESCREVA APENAS OS PRODUTOS LISTADOS ABAIXO:

{produtos_texto}

REGRAS ESTRITAS:
1. Use APENAS as informações dos produtos listados
2. Não invente nenhuma característica
3. Não mencione cores, tipos ou preços que não estão na lista
4. Seja natural e direto
5. Descreva cada produto brevemente
6. INCLUA O PREÇO de cada produto

DESCRIÇÃO:"""

    def _chamar_ollama_controlado(self, prompt: str) -> str:
        """Chamada com configurações balanceadas"""
        payload = {
            "model": self.model, 
            "prompt": prompt, 
            "stream": False,
            "options": {
                "temperature": 0.3,       # Um pouco mais flexível
                "top_p": 0.7,
                "num_predict": 150,       # Mais tokens para descrições
                "seed": 42,
                "repeat_penalty": 1.2     # Reduz repetição
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception(f"Serviço indisponível: {response.status_code}")
            
            return response.json()["response"].strip()
        except requests.exceptions.Timeout:
            raise Exception("Timeout na chamada do Ollama")
        except Exception as e:
            raise Exception(f"Erro na chamada: {str(e)}")

    def _validar_resposta_rigorosa(self, resposta: str, produtos: list) -> str:
        """Validação extremamente rigorosa"""
        resposta = resposta.strip()
        
        # Remove prefixos comuns
        for prefix in ["DESCRIÇÃO:", "RESPOSTA:", "```"]:
            if resposta.startswith(prefix):
                resposta = resposta[len(prefix):].strip()
        
        # Verificação básica de qualidade
        if len(resposta) < 25:
            raise Exception("Resposta muito curta")
        
        # Verifica se menciona produtos inexistentes
        termos_produtos = set()
        for p in produtos:
            termos_produtos.update(p.descricao.lower().split())
            termos_produtos.add(p.cor.lower())
        
        palavras_resposta = set(resposta.lower().split())
        palavras_estranhas = palavras_resposta - termos_produtos - {
            "camisa", "camisas", "preço", "r$", "cor", "manga", "curta", 
            "longa", "social", "polo", "normal", "tem", "temos", "encontrei",
            "produto", "produtos", "descrição", "lista", "apenas"
        }
        
        if len(palavras_estranhas) > 5:  # Muitas palavras não relacionadas
            raise Exception("Resposta contém informações não relacionadas")
        
        return resposta

    def _resposta_direta(self, produtos: list) -> str:
        """Resposta 100% baseada em dados - zero alucinações"""
        if len(produtos) == 1:
            p = produtos[0]
            return f"Temos: {p.descricao} - R$ {p.preco:.2f}"
        
        if len(produtos) <= 3:
            descricoes = []
            for p in produtos:
                descricoes.append(f"- {p.descricao} - R$ {p.preco:.2f}")
            return "Encontrei as seguintes camisas:\n" + "\n".join(descricoes)
        
        # Para mais produtos, agrupar por tipo
        grupos = {}
        for p in produtos[:6]:  # Limitar a 6 produtos
            tipo = p.tipo.capitalize()
            if tipo not in grupos:
                grupos[tipo] = []
            grupos[tipo].append(p)
        
        resposta = f"Encontrei {len(produtos)} camisas:\n"
        for tipo, prods in grupos.items():
            resposta += f"\n{tipo}:\n"
            for p in prods[:2]:  # Máximo 2 por tipo
                resposta += f"- {p.descricao} - R$ {p.preco:.2f}\n"
        
        return resposta
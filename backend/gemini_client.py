# gemini_client.py - AGENTE HUMANIZADO E NATURAL
import google.generativeai as genai
import os
import logging
import random
from typing import List
from models import Produto

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, model="gemini-pro"):
        self.api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCz2pZJ_Uq1ZR77azSU9nTVm5l_memKmDE")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY não encontrada - usando respostas naturais")
            self.model = None
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model)
            logger.info("Assistente humanizado inicializado")
        except Exception as e:
            logger.warning(f"Erro ao inicializar Gemini: {e}. Usando respostas naturais.")
            self.model = None

    def generate(self, produtos: List[Produto], query_original: str = "") -> str:
        """
        Gera resposta completamente natural como uma pessoa real
        """
        try:
            logger.info(f"Assistente processando: '{query_original}'")
            
            if not produtos:
                return self._resposta_sem_produtos(query_original)
            
            # Se temos Gemini, usa IA para resposta natural
            if self.model is not None:
                return self._gerar_resposta_humanizada(produtos, query_original)
            else:
                return self._resposta_natural_fallback(produtos, query_original)
            
        except Exception as e:
            logger.warning(f"Erro na geração: {e}")
            return self._resposta_natural_fallback(produtos, query_original)

    def _gerar_resposta_humanizada(self, produtos: List[Produto], query: str) -> str:
        """Gera resposta completamente natural como um vendedor real"""
        
        contexto = self._preparar_contexto_natural(produtos)
        
        prompt = f"""
        VOCÊ É: Ana, uma vendedora experiente de uma loja de camisas. Você é simpática, prestativa e fala EXATAMENTE como uma pessoa real, não como um robô.

        SEU ESTILO DE CONVERSA:
        - Fala natural, como numa conversa de WhatsApp
        - Usa emojis moderadamente 😊👍👕
        - É calorosa e empática
        - Faz perguntas de follow-up naturalmente
        - Usa gírias leves quando cabe ("show", "legal", "top")
        - É organizada mas não robótica

        PRODUTOS QUE TEMOS NO MOMENTO:
        {contexto}

        CLIENTE PERGUNTOU: "{query}"

        SUA RESPOSTA DEVE SER:
        - 100% natural, como se estivesse conversando com um amigo
        - Use APENAS os produtos que listei acima
        - Seja útil e dê informações concretas
        - Mostre entusiasmo genuíno pelos produtos
        - Se for muita informação, organize de forma natural
        - Termine com uma pergunta ou sugestão natural

        NÃO USE:
        - "Baseado na sua pergunta"
        - "Conforme solicitado"
        - Listas muito formais
        - Linguagem robótica

        EXEMPLOS DE COMO FALAR:
        "Oi! Então, temos várias opções legais..."
        "Olha, das camisas polo temos..."
        "Que bom que perguntou! Temos..."
        "Vou te mostrar o que temos aqui..."
        "E aí, beleza? Das camisas..."

        AGORA RESPONDA EXATAMENTE COMO A ANA, A VENDEDORA:
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # Mais criativo e natural
                    top_p=0.9,
                    max_output_tokens=600,
                )
            )
            
            if not response.text:
                raise Exception("Resposta vazia")
                
            resposta = response.text.strip()
            
            # Garante que a resposta seja natural
            if self._resposta_muito_robotica(resposta):
                return self._resposta_natural_fallback(produtos, query)
                
            return resposta
            
        except Exception as e:
            logger.error(f"Erro no Gemini: {e}")
            return self._resposta_natural_fallback(produtos, query)

    def _preparar_contexto_natural(self, produtos: List[Produto]) -> str:
        """Prepara contexto de forma natural para a IA"""
        
        catalogo = {}
        for produto in produtos:
            if produto.tipo not in catalogo:
                catalogo[produto.tipo] = {}
            if produto.variante not in catalogo[produto.tipo]:
                catalogo[produto.tipo][produto.variante] = []
            catalogo[produto.tipo][produto.variante].append(produto)
        
        contexto = ""
        
        for tipo, variantes in catalogo.items():
            contexto += f"\n{tipo.upper()}:\n"
            
            for variante, produtos_variante in variantes.items():
                preco_min = min(p.preco for p in produtos_variante)
                preco_max = max(p.preco for p in produtos_variante)
                cores = list(set(p.cor for p in produtos_variante))
                
                contexto += f"- {variante}: R$ {preco_min:.2f} a R$ {preco_max:.2f} "
                contexto += f"(cores: {', '.join(cores)})\n"
        
        contexto += f"\nTotal: {len(produtos)} camisas no momento"
        
        return contexto

    def _resposta_natural_fallback(self, produtos: List[Produto], query: str) -> str:
        """Resposta natural quando não tem IA"""
        
        saudacoes = [
            "Oi! 😊 ",
            "Olá! ",
            "E aí! ",
            "Oi, tudo bem? ",
            "Olá, que bom que veio! "
        ]
        
        introducoes = [
            "Vou te mostrar o que temos aqui...",
            "Deixa eu ver aqui nossas opções...",
            "Tenho algumas opções legais pra você...",
            "Vamos lá, tenho boas opções...",
            "Olha só o que encontrei pra você..."
        ]
        
        resposta = random.choice(saudacoes) + random.choice(introducoes) + "\n\n"
        
        # Agrupa de forma natural
        catalogo = {}
        for produto in produtos:
            if produto.tipo not in catalogo:
                catalogo[produto.tipo] = []
            catalogo[produto.tipo].append(produto)
        
        for tipo, prods in catalogo.items():
            if tipo.lower() == 'polo':
                resposta += f"👕 **Camisas Polo:**\n"
            elif tipo.lower() == 'social':
                resposta += f"💼 **Camisas Sociais:**\n"
            elif tipo.lower() == 'casual':
                resposta += f"😎 **Camisas Casuais:**\n"
            elif tipo.lower() == 'esportiva':
                resposta += f"🏃 **Camisas Esportivas:**\n"
            else:
                resposta += f"⭐ **{tipo.title()}:**\n"
            
            # Agrupa por variante dentro do tipo
            variantes = {}
            for p in prods:
                if p.variante not in variantes:
                    variantes[p.variante] = []
                variantes[p.variante].append(p)
            
            for variante, prods_variante in variantes.items():
                preco_min = min(p.preco for p in prods_variante)
                preco_max = max(p.preco for p in prods_variante)
                cores = list(set(p.cor for p in prods_variante))
                
                resposta += f"   • {variante}: R$ {preco_min:.2f}"
                if preco_max != preco_min:
                    resposta += f" a R$ {preco_max:.2f}"
                
                if cores:
                    resposta += f" - cores: {', '.join(cores[:3])}"
                    if len(cores) > 3:
                        resposta += f" e mais {len(cores)-3}"
                resposta += "\n"
            
            resposta += "\n"
        
        # Final natural
        finais = [
            f"\nNo total tenho {len(produtos)} opções pra você! Qual tipo te interessa mais? 😊",
            f"\nEssas são nossas {len(produtos)} melhores opções! Tem alguma que chamou sua atenção?",
            f"\nSão {len(produtos)} camisas bem legais! Qual você quer saber mais?",
            f"\nGostou de alguma dessas {len(produtos)} opções? Posso te dar mais detalhes!",
        ]
        
        resposta += random.choice(finais)
        
        return resposta

    def _resposta_sem_produtos(self, query: str) -> str:
        """Resposta quando não encontra produtos"""
        
        respostas_empaticas = [
            f"Poxa, não encontrei nada com '{query}' no momento 😕\n\nMas tenho muitas camisas legais! Pode me perguntar por:\n• Tipo: polo, social, casual\n• Cor: azul, preta, branca, etc.\n• Preço: até R$ 100, por exemplo\n\nO que você tá procurando? 😊",
            
            f"Hmm, não achei camisas com '{query}'... 🤔\n\nQue tal tentar:\n• \"camisas polo\"\n• \"sociais azuis\"\n• \"até R$ 150\"\n• \"casuais estampadas\"\n\nMe conta melhor o que você precisa! 👕",
            
            f"Vish, não tenho nada com '{query}' agora 😅\n\nMas olha o que tenho disponível:\n🎯 Polo básica e premium\n💼 Sociais formais\n😎 Casuais do dia a dia\n🏃 Esportivas\n\nQual tipo te interessa?",
            
            f"Ops! Não encontrei '{query}' no estoque...\n\nMas tenho umas camisas bem tops! Pode me perguntar por:\n• \"mostre as polo\"\n• \"quanto custa as sociais\"\n• \"tem em preto?\"\n• \"camisas baratas\"\n\nVamos encontrar a ideal pra você! 💪"
        ]
        
        return random.choice(respostas_empaticas)

    def _resposta_muito_robotica(self, resposta: str) -> bool:
        """Detecta se a resposta é muito robótica"""
        indicadores_robotica = [
            "baseado na sua pergunta",
            "conforme solicitado", 
            "de acordo com os dados",
            "segue a lista",
            "conforme informado",
            "com base em",
            "de acordo com sua solicitação"
        ]
        
        resposta_lower = resposta.lower()
        for indicador in indicadores_robotica:
            if indicador in resposta_lower:
                return True
        return False
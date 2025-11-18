# Sistema de Chat para Loja de Camisas

Sistema de atendimento virtual para loja de camisas utilizando RAG (Retrieval-Augmented Generation) e Ollama para fornecer recomendações precisas de produtos.

## Tecnologias Utilizadas

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **IA**: Ollama com modelo TinyLlama
- **Banco de Dados**: SQLite
- **Busca Semântica**: Sentence Transformers
- **Vector Store**: FAISS

## Pré-requisitos

- Python 3.8+
- Node.js 16+
- Ollama instalado e configurado

Chat_Bot_/
├── backend/
│   ├── main.py              # Aplicação FastAPI
│   ├── rag.py               # Pipeline RAG
│   ├── ollama_client.py     # Cliente Ollama
│   ├── populate.py          # População do banco
│   ├── requirements.txt     # Dependências Python
│   └── database/           # Arquivos de banco
└── frontend/
    ├── src/
    │   ├── App.jsx         # Componente principal
    │   ├── main.jsx        # Ponto de entrada
    │   ├── components/     # Componentes React
    │   ├── services/       # API client
    │   └── styles/         # Estilos CSS
    ├── package.json        # Dependências Node.js
    └── index.html          # HTML principal
    
## Instalação do Ollama

```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Iniciar serviço Ollama
ollama serve

# Baixar modelo (em outro terminal)
ollama pull tinyllama

# Navegar para o diretório do backend
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar o backend
uvicorn main:app --reload --port 8000

# Navegar para o diretório do frontend (em outro terminal)
cd frontend

# Instalar dependências
npm install

# Executar o frontend
npm run dev
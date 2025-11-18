import React, { useState } from "react"
import Chat from './components/Chat'
import { initializeDatabase } from './services/api'
import './styles/App.css'

function App() {
    const [isInitialized, setInitialized] = useState(false)
    const [loading, setLoading] = useState(false)
    const [status, setStatus] = useState('')

    const handleInitialize = async () => {
        setLoading(true)
        setStatus('Conectando com o servidor...')
        
        try {
            setStatus('Inicializando banco de dados...')
            const result = await initializeDatabase()
            console.log('✅ Resultado da inicialização:', result)
            
            setStatus('Sistema pronto!')
            setTimeout(() => {
                setInitialized(true)
            }, 1000)
            
        } catch (error) {
            console.error('❌ Erro na inicialização:', error)
            setStatus(`Erro: ${error.message}`)
            
            // Pergunta se quer continuar em modo simulação
            const shouldContinue = window.confirm(`${error.message}\n\nDeseja continuar em modo de simulação?`)
            if (shouldContinue) {
                setInitialized(true)
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app">
            <header className="app-header">
                <h1>Assistente Virtual de Vendas</h1>
                <p>Encontre a camisa perfeita com a minha ajuda especializada!</p>
            </header>
            <main className="app-main">
                {!isInitialized ? (
                    <div className="init-section">
                        <div className="init-card">
                            <h2>Bem-vindo à Loja de Camisas!</h2>
                            <p>Para começar, vamos inicializar o sistema de recomendações</p>
                            
                            {status && (
                                <div style={{
                                    padding: '1rem',
                                    margin: '1rem 0',
                                    background: status.includes('Erro') ? '#ffe6e6' : '#f0f8ff',
                                    borderRadius: '8px',
                                    border: status.includes('Erro') ? '1px solid #ffcccc' : '1px solid #cce7ff',
                                    color: status.includes('Erro') ? '#cc0000' : '#0066cc'
                                }}>
                                    {status}
                                </div>
                            )}
                            
                            <button
                                onClick={handleInitialize}
                                disabled={loading}
                                className="init-button"
                            >
                                {loading ? 'Inicializando...' : 'Inicializar Sistema'}
                            </button>
                        </div>
                    </div>
                ) : (
                    <Chat />
                )}
            </main>
            <footer className="app-footer">
                <p>Powered by RAG + Ollama | Gustavo Holanda de Sousa</p>
            </footer>
        </div>
    )
}

export default App
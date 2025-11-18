import React,{ useState, useEffect} from "react"
import Chat from './components/Chat'
import { initializeDataBase} from './services/api'
import './styles/App.css'

function App() {
    const [isInitialized, setInitialized] = useState(false)
    const [loading, setLoading] = useState(false)

    const handleInitialize = async() => {
        setLoading(true)
        try {
            await initializeDataBase()
            setInitialized(true)
        }
        catch (error) {
            console.error ('Erro ao inicializar o banco:', error)
            alert('Erro ao incializar o banco de dados')
        
        } finally{
            setLoading(false)
        }
    }
    retutn (
        <div className="app">
            <header className="app-header">
                <h1>Assistente Virtual de Vendas</h1>
                <p>Encontre a camisa perfeita com a minha ajuda especializada!</p>
            </header>
            <main className="app-main">
                {!isInitialized ? (
                    <div className="init-section">
                        <div className="init-card">
                            <h2>Bem-vindo!</h2>
                            <p>Para começar, vamos inicializar o banco de dados com nossos produtos</p>
                            <button
                                onClick={handleInitialize}
                                disabled={loading}
                                className="init-button"
                            >
                                {loading ? 'Inicializando...' : 'Inicializar Sistema'}
                            </button>
                        </div>
                    </div>
                ):(
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
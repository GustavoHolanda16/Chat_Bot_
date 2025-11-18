import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000,
})

export const initializeDatabase = async () => {
    try {
        console.log('🔄 Inicializando banco de dados...')
        const response = await api.post('/prepare-db')
        console.log('✅ Backend respondeu:', response.data)
        return response.data
    } catch (error) {
        console.error('❌ Erro ao inicializar banco:', error.response?.data || error.message)
        throw new Error(error.response?.data?.detail || 'Falha na inicialização do banco')
    }
}

export const sendMessage = async (message) => {
    try {
        console.log('📤 Enviando mensagem para o chat:', message)
        const response = await api.get('/chat', {
            params: { q: message }
        })
        console.log('📥 Resposta recebida:', response.data)
        
        // SEU BACKEND USA "resposta" EM VEZ DE "response"
        return {
            response: response.data.resposta || "Não foi possível obter resposta",
            produtos_encontrados: response.data.produtos_encontrados || 0
        }
        
    } catch (error) {
        console.error('❌ Erro no chat:', error.response?.data || error.message)
        throw new Error('Erro ao comunicar com o servidor')
    }
}

export default api
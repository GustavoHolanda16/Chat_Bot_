import axios from  'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

export const sendMenssage = async(message) => {
    const response = await api.get('/chat', {
        params: {q: message}
    })
    return response 
}

export default api 
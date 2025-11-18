import React, { useState, useRef, useEffect } from 'react'
import Message from './Message.jsx'
import { sendMessage } from '../services/api'

const Chat = () => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            text: 'Olá! Sou seu assistente virtual de vendas. Posso ajudar você a encontrar a camisa perfeita!',
            isUser: false,
            timestamp: new Date()
        }
    ])
    const [inputMessage, setInputMessage] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSendMessage = async (e) => {
        e.preventDefault()
        if (!inputMessage.trim() || isLoading) return

        console.log('📤 Enviando mensagem:', inputMessage)

        // Adiciona mensagem do usuário
        const userMessage = {
            id: Date.now(),
            text: inputMessage,
            isUser: true,
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setInputMessage('')
        setIsLoading(true)

        try {
            // Adiciona mensagem de loading do bot
            const loadingMessage = {
                id: Date.now() + 1,
                text: '...',
                isUser: false,
                timestamp: new Date(),
                isLoading: true
            }
            setMessages(prev => [...prev, loadingMessage])

            // Chama a API
            const response = await sendMessage(inputMessage)
            console.log('✅ Resposta da API:', response)

            // Substitui a mensagem de loading pela resposta real
            setMessages(prev => prev.map(msg => 
                msg.id === loadingMessage.id 
                    ? { 
                        ...msg, 
                        text: response.response,
                        isLoading: false 
                      }
                    : msg
            ))

        } catch (error) {
            console.error('❌ Erro no chat:', error)
            
            // Remove a mensagem de loading e adiciona erro
            setMessages(prev => prev.filter(msg => !msg.isLoading))
            
            const errorMessage = {
                id: Date.now() + 1,
                text: "Desculpe, estou com problemas técnicos. Tente novamente em alguns instantes.",
                isUser: false,
                timestamp: new Date()
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className='chat-container'>
            <div className='chat-messages'>
                {messages.map((message) => (
                    <Message
                        key={message.id}
                        text={message.text}
                        isUser={message.isUser}
                        timestamp={message.timestamp}
                        isLoading={message.isLoading}
                    />
                ))}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className='chat-input-form'>
                <div className='input-container'>
                    <input
                        type='text'
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder='Digite sua mensagem...'
                        disabled={isLoading}
                        className='chat-input'
                    />
                    <button
                        type='submit'
                        disabled={!inputMessage.trim() || isLoading}
                        className='send-button'
                    >
                        {isLoading ? '...' : '>'}
                    </button>
                </div>
            </form>
        </div>
    )
}

export default Chat
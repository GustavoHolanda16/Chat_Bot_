import React, { useState, useRef, useEffect} from 'react'
import Message from './Message'
import { sendMessage } from '../services/api'
import { getNativeElementReferenceFromReactNativeDocumentElementInstanceHandle } from 'react-native/types_generated/src/private/webapis/dom/nodes/internals/ReactNativeDocumentElementInstanceHandle'

const Chat = () => {
    const [messages, setMessages] = useState([
        {
            id:1,
            text: 'Olá! Sou um vendedor virtual da loja. Como posso ajudá-lo? ',
            isUser : false,
            timestamp: new Date()
        }
    ])
    const [inputMessage, setInputMessage] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth"})

    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSendMessage = async (e) => {
        e.preventDefault()

        if (!inputMessage.trim() || isLoading) return

        const userMessage = {
            id: DAte.now(),
            text: inputMessage,
            isUser: true,
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setInputMessage('')
        setIsLoading(true)

        try {
            const response = await sendMessage(inputMessage)
            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let assistantMessage = ''

            const botMessage = {
                id: Date.now() +1,
                text: '',
                isUser: false,
                timestamp: new Date()
            }

            setMessages(prev => [...prev, botMessage])

            while (true) {
                const {done, value} = await reader.read()
                if (done) break

                const chunk = decoder.decode(value)
                const lines = chuck.split('\n')

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6))
                            assistantMessage += data.data

                            setMessages(prev => prev.map(msg =>
                                msg.id === botMessage.id
                                ?{ ...msg, text: assistantMessage}
                                : msg
                            ))
                        } catch (e){
                        }
                    }
                }
            }
        }catch (error){
            console.error('Error ao enviar mensagem:', error)
            const errorMessage = {
                id: Date.now() +1,
                text: "Desculpe, ocorreu um erro ao processsar sua mensagem. Tente novamente",
                isUser: false,
                timestamp: new Date()
            }
            setMessages(prev => [...prev, errorMessage])
        }finally{
            setIsLoading(false)
        }
    }
    return (
        <div className='chat-container'>
            <div className='chat-messages'>
                {messages.map((message) =>(
                    <message
                        key = {message.id}
                        text = {message.text}
                        isUser = {message.isUser}
                        timestamp = {message.timestamp}
                    />
                ))}
                {isLoading && (
                    <message
                        text = '...'
                        isUser = {false}
                        timestamp = {new Date()}
                        isLoading= {true}    
                    />
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className='chat-input-form'>
                <div className='input-container'>
                    <input
                        type='text'
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder='Digite sua mensagem'
                        disabled={isLoading}
                        className='chat-input'
                    />
                    <button
                        type='submit'
                        disabled={!inputMessage.trim() || isLoading}
                        className='send-button'
                    >
                        {isLoading ? 'Aguarde': '>'}
                    </button>
                </div>
            </form>
        </div>
    )
}

export default Chat
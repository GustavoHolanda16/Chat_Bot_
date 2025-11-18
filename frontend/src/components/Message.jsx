import React from "react"

const Message = ({text, isUser, timestamp, isLoading = false}) => {
    return (
        <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
            <div className="message-avatar">
                {isUser ? '👤' : '🤖'}
            </div>
            <div className="message-content">
                <div className="messagen-text">
                    {isLoading ? (
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    ):(
                        text
                    )}
                </div>
                <div className="message-time">
                    {timestamp.toLocaleTimeString('pt-BR',{
                        hour: '2-digit',
                        minute: '2-digit'
                    })}
                </div>
            </div>
        </div>

    )
}

export default Message
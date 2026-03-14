import React, { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { api } from '../api'
import '../styles/Chatbot.css'

const PREDEFINED_QUESTIONS = [
  "I'm getting VPN error 422 when trying to connect",
  "I need to reset my password",
  "My WiFi is slow",
  "How do I install software?",
  "I'm seeing error code 0x80070005",
]

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState('demo@acmecorp.com')
  const [isLoading, setIsLoading] = useState(false)
  const [showQuestions, setShowQuestions] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  useEffect(() => scrollToBottom(), [messages])

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setShowQuestions(true)
    }
  }, [isOpen, messages.length])

  const handlePredefinedQuestion = (questionText: string) => {
    setInput('')
    setShowQuestions(false)
    setMessages((prev) => [...prev, { role: 'user', content: questionText }])
    setIsLoading(true)

    api
      .post<{ response: string; session_id: string }>('/chat', {
        message: questionText,
        session_id: sessionId ?? undefined,
        user_email: userEmail,
      })
      .then(({ data }) => {
        setSessionId(data.session_id)
        setMessages((prev) => [...prev, { role: 'assistant', content: data.response }])
      })
      .catch(() => {
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: 'Sorry, I encountered an error. Please ensure the backend is running on port 8000.' },
        ])
      })
      .finally(() => setIsLoading(false))
  }

  const handleSendMessage = async (e: React.FormEvent, questionText?: string) => {
    e?.preventDefault()
    const messageToSend = questionText ?? input.trim()
    if (!messageToSend || isLoading) return

    const userMessage = messageToSend.trim()
    setInput('')
    setShowQuestions(false)
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    try {
      const { data } = await api.post<{ response: string; session_id: string }>('/chat', {
        message: userMessage,
        session_id: sessionId ?? undefined,
        user_email: userEmail,
      })
      setSessionId(data.session_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please ensure the backend is running on port 8000.' },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <button
        className="chatbot-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        💬
      </button>

      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>IT Support Chatbot</h3>
            <div className="chatbot-header-email">
              <label>Email:</label>
              <input
                type="email"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
                className="chatbot-email-input"
              />
            </div>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 && showQuestions && (
              <div className="chatbot-welcome">
                <p>Hello! I'm your IT Support assistant. How can I help you today?</p>
                <div className="predefined-questions">
                  <p className="questions-label">Common questions:</p>
                  <div className="questions-grid">
                    {PREDEFINED_QUESTIONS.map((q, i) => (
                      <button
                        key={i}
                        className="question-button"
                        onClick={() => handlePredefinedQuestion(q)}
                        disabled={isLoading}
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
            {messages.length === 0 && !showQuestions && (
              <div className="chatbot-welcome">
                <p>Hello! I'm your IT Support assistant. How can I help you today?</p>
              </div>
            )}
            {messages.length > 0 && showQuestions && (
              <div className="predefined-questions-inline">
                <div className="questions-header">
                  <p className="questions-label">Common questions:</p>
                  <button
                    className="hide-questions-button"
                    onClick={() => setShowQuestions(false)}
                    aria-label="Hide questions"
                    title="Hide questions"
                  >
                    ×
                  </button>
                </div>
                <div className="questions-grid">
                  {PREDEFINED_QUESTIONS.map((q, i) => (
                    <button
                      key={i}
                      className="question-button"
                      onClick={() => handlePredefinedQuestion(q)}
                      disabled={isLoading}
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role === 'user' ? 'message-user' : 'message-assistant'}`}
              >
                <div className="message-content">
                  {message.role === 'assistant' ? (
                    <div className="message-markdown">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message message-assistant">
                <div className="message-content">
                  <span className="typing-indicator">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-form" onSubmit={(e) => handleSendMessage(e)}>
            {messages.length > 0 && !showQuestions && (
              <button
                type="button"
                className="show-questions-button"
                onClick={() => setShowQuestions(true)}
                disabled={isLoading}
                aria-label="Show common questions"
                title="Show common questions"
              >
                📋
              </button>
            )}
            <input
              type="text"
              className="chatbot-input"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="chatbot-send"
              disabled={isLoading || !input.trim()}
              aria-label="Send message"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  )
}

export default Chatbot

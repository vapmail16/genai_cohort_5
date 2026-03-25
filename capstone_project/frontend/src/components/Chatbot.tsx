import React, { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { api } from '../api'
import '../styles/Chatbot.css'

export type ChatApiResponse = {
  response: string
  session_id: string
  sources?: string[]
  demo_track?: string | null
  presenter?: Record<string, string> | null
  mcp_trace?: {
    tool?: string | null
    success?: boolean
    result_summary?: string
  } | null
}

export type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
  presenter?: Record<string, string>
  mcp_trace?: ChatApiResponse['mcp_trace']
}

const PREDEFINED_QUESTIONS = [
  "I'm getting VPN error 422 when trying to connect",
  "I need to reset my password",
  "My WiFi is slow",
  "How do I install software?",
  "I'm seeing error code 0x80070005",
]

const DEMO_PRESETS: { label: string; message: string; demo_track?: string }[] = [
  { label: 'Demo menu', message: 'Hi' },
  { label: 'Plain LLM', message: 'Give one password best practice in one sentence.', demo_track: 'plain_llm' },
  { label: 'KB RAG', message: "I'm getting VPN error 422 when trying to connect", demo_track: 'rag_kb' },
  {
    label: 'DB RAG',
    message: 'Summarize recent internal tickets that mention VPN or network.',
    demo_track: 'rag_db',
  },
  { label: 'Agentic MCP', message: 'Check my VPN status', demo_track: 'agentic_mcp' },
]

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
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

  const postChat = async (message: string, demo_track?: string) => {
    const { data } = await api.post<ChatApiResponse>('/chat', {
      message,
      session_id: sessionId ?? undefined,
      user_email: userEmail,
      demo_mode: true,
      ...(demo_track ? { demo_track } : {}),
    })
    return data
  }

  const handleDemoPreset = (preset: (typeof DEMO_PRESETS)[number]) => {
    setInput('')
    setShowQuestions(false)
    const visible = preset.demo_track
      ? `[${preset.label}] ${preset.message}`
      : preset.message
    setMessages((prev) => [...prev, { role: 'user', content: visible }])
    setIsLoading(true)
    postChat(preset.message, preset.demo_track)
      .then((data) => {
        setSessionId(data.session_id)
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: data.response,
            presenter: data.presenter ?? undefined,
            mcp_trace: data.mcp_trace ?? undefined,
          },
        ])
      })
      .catch(() => {
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: 'Sorry, I encountered an error. Is the backend running on port 8000?' },
        ])
      })
      .finally(() => setIsLoading(false))
  }

  const handlePredefinedQuestion = (questionText: string) => {
    setInput('')
    setShowQuestions(false)
    setMessages((prev) => [...prev, { role: 'user', content: questionText }])
    setIsLoading(true)

    postChat(questionText)
      .then((data) => {
        setSessionId(data.session_id)
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: data.response,
            presenter: data.presenter ?? undefined,
            mcp_trace: data.mcp_trace ?? undefined,
          },
        ])
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
      const data = await postChat(userMessage)
      setSessionId(data.session_id)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          presenter: data.presenter ?? undefined,
          mcp_trace: data.mcp_trace ?? undefined,
        },
      ])
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
                <div className="chatbot-demo-strip">
                  <p className="demo-strip-label">Oxford / cohort demo tracks</p>
                  <div className="demo-strip-buttons">
                    {DEMO_PRESETS.map((p) => (
                      <button
                        key={p.label}
                        type="button"
                        className="demo-track-button"
                        onClick={() => handleDemoPreset(p)}
                        disabled={isLoading}
                      >
                        {p.label}
                      </button>
                    ))}
                  </div>
                </div>
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
                    <>
                      <div className="message-markdown">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                      </div>
                      {(message.presenter || message.mcp_trace) && (
                        <details className="chatbot-presenter-details">
                          <summary>Presenter / code &amp; MCP trace</summary>
                          {message.presenter && (
                            <pre className="chatbot-meta-block">
                              {JSON.stringify(message.presenter, null, 2)}
                            </pre>
                          )}
                          {message.mcp_trace && (
                            <pre className="chatbot-meta-block">
                              {JSON.stringify(message.mcp_trace, null, 2)}
                            </pre>
                          )}
                        </details>
                      )}
                    </>
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

import { useState, useRef, useEffect } from 'react'
import { roadmapAPI } from '../services/api.js'

const STARTER_PROMPTS = [
  'How do I get started with my roadmap?',
  'What should I focus on this week?',
  'Explain a concept from my current step',
  'How do I practice my skills effectively?',
  'What projects can I build to learn faster?',
]

export default function CoachChat({ studentId }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm your LearnMate AI coach, powered by IBM Granite. Ask me anything about your learning journey — course recommendations, concept explanations, motivation tips, or study strategies. How can I help you today?",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text) => {
    const userText = text || input.trim()
    if (!userText) return

    const userMsg = { role: 'user', content: userText }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await roadmapAPI.chat({ student_id: studentId, message: userText })
      setMessages((prev) => [...prev, { role: 'assistant', content: res.data.response }])
    } catch (err) {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: '⚠️ I had trouble connecting to IBM Granite. Please check the backend is running and your API keys are configured.',
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ marginBottom: 4 }}>AI Learning Coach</h1>
        <p className="text-muted">Powered by IBM Granite — your personal learning advisor</p>
      </div>

      {/* Starter prompts */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 16 }}>
        {STARTER_PROMPTS.map((prompt) => (
          <button key={prompt} onClick={() => sendMessage(prompt)}
            style={{
              background: 'white', border: '1.5px solid #e2e8f0', borderRadius: 99,
              padding: '6px 14px', fontSize: '0.82rem', cursor: 'pointer',
              color: '#1a6cf6', fontWeight: 500, transition: 'all 0.15s',
            }}>{prompt}</button>
        ))}
      </div>

      {/* Chat window */}
      <div style={{
        background: 'white', border: '1px solid #e2e8f0', borderRadius: 16,
        height: 420, overflowY: 'auto', padding: 20,
        display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 16,
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
          }}>
            {msg.role === 'assistant' && (
              <div style={{
                width: 32, height: 32, borderRadius: '50%',
                background: 'linear-gradient(135deg, #1a6cf6, #6d28d9)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: 'white', fontSize: '0.8rem', fontWeight: 800, marginRight: 8, flexShrink: 0,
              }}>L</div>
            )}
            <div className={`chat-bubble ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}`}
              style={{ whiteSpace: 'pre-wrap' }}>
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{
              width: 32, height: 32, borderRadius: '50%',
              background: 'linear-gradient(135deg, #1a6cf6, #6d28d9)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: 'white', fontSize: '0.8rem', fontWeight: 800, flexShrink: 0,
            }}>L</div>
            <div className="chat-bubble chat-bubble-ai" style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
              <span style={{ animation: 'pulse 1s infinite', animationDelay: '0ms', width: 8, height: 8, background: '#94a3b8', borderRadius: '50%', display: 'inline-block' }} />
              <span style={{ animation: 'pulse 1s infinite', animationDelay: '200ms', width: 8, height: 8, background: '#94a3b8', borderRadius: '50%', display: 'inline-block' }} />
              <span style={{ animation: 'pulse 1s infinite', animationDelay: '400ms', width: 8, height: 8, background: '#94a3b8', borderRadius: '50%', display: 'inline-block' }} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: 10 }}>
        <input
          className="form-input"
          style={{ flex: 1 }}
          placeholder="Ask your AI coach anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() } }}
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
      <p className="text-xs text-muted" style={{ marginTop: 8, textAlign: 'right' }}>
        Powered by IBM Granite • Press Enter to send
      </p>
      <style>{`@keyframes pulse { 0%,100%{opacity:0.3} 50%{opacity:1} }`}</style>
    </div>
  )
}

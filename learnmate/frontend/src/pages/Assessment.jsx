import { useState } from 'react'
import { studentAPI } from '../services/api.js'

const DOMAINS = [
  'Frontend Development', 'Backend Development', 'Full Stack Development',
  'Data Science & ML', 'Cybersecurity', 'UI/UX Design',
  'Mobile Development', 'Cloud & DevOps',
]

const RATINGS = [
  { value: 1, label: 'Complete Beginner', desc: 'No prior knowledge', color: '#94a3b8' },
  { value: 2, label: 'Beginner', desc: 'Some basic concepts', color: '#3b82f6' },
  { value: 3, label: 'Intermediate', desc: 'Comfortable with basics', color: '#8b5cf6' },
  { value: 4, label: 'Advanced', desc: 'Built real projects', color: '#f59e0b' },
  { value: 5, label: 'Expert', desc: 'Professional experience', color: '#16a34a' },
]

export default function Assessment({ studentId }) {
  const [domain, setDomain] = useState('')
  const [rating, setRating] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [chatMode, setChatMode] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [assessmentDone, setAssessmentDone] = useState(false)

  const runQuickAssess = async () => {
    if (!domain || !rating) return
    setLoading(true)
    setError('')
    try {
      const res = await studentAPI.quickAssess(studentId, { domain, self_rating: rating })
      setResult(res.data.assessment)
    } catch (err) {
      setError(err.response?.data?.error || 'Assessment failed.')
    } finally {
      setLoading(false)
    }
  }

  const startChatAssessment = async () => {
    if (!domain) return
    setChatLoading(true)
    try {
      const res = await studentAPI.startAssessment(studentId, { domain })
      setChatMessages([{ role: 'assistant', content: res.data.message }])
      setChatMode(true)
    } catch (err) {
      setError('Failed to start assessment.')
    } finally {
      setChatLoading(false)
    }
  }

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return
    const msg = chatInput
    setChatMessages((prev) => [...prev, { role: 'user', content: msg }])
    setChatInput('')
    setChatLoading(true)
    try {
      const res = await studentAPI.chatAssessment(studentId, { message: msg })
      setChatMessages((prev) => [...prev, { role: 'assistant', content: res.data.message }])
      if (res.data.assessment_complete) {
        setResult(res.data.assessment)
        setAssessmentDone(true)
      }
    } catch (_) {
      setChatMessages((prev) => [...prev, { role: 'assistant', content: 'Error processing response.' }])
    } finally {
      setChatLoading(false)
    }
  }

  const levelColor = { beginner: '#3b82f6', intermediate: '#8b5cf6', advanced: '#f59e0b', expert: '#16a34a' }

  return (
    <div style={{ maxWidth: 720, margin: '0 auto' }}>
      <h1 style={{ marginBottom: 4 }}>Skill Assessment</h1>
      <p className="text-muted" style={{ marginBottom: 24 }}>
        Let IBM Granite AI evaluate your current skill level and personalize your roadmap.
      </p>

      {!chatMode && !result && (
        <div className="card" style={{ marginBottom: 20 }}>
          <h2 style={{ marginBottom: 16 }}>Select Domain</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 24 }}>
            {DOMAINS.map((d) => (
              <span key={d} className={`chip ${domain === d ? 'selected' : ''}`} onClick={() => setDomain(d)}>
                {d}
              </span>
            ))}
          </div>

          {domain && (
            <>
              <h2 style={{ marginBottom: 12 }}>Rate Your Level in {domain}</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
                {RATINGS.map((r) => (
                  <div key={r.value} onClick={() => setRating(r.value)}
                    style={{
                      padding: '14px 18px', borderRadius: 10, cursor: 'pointer',
                      border: `2px solid ${rating === r.value ? r.color : '#e2e8f0'}`,
                      background: rating === r.value ? `${r.color}15` : 'white',
                      display: 'flex', alignItems: 'center', gap: 14, transition: 'all 0.15s',
                    }}>
                    <span style={{
                      width: 36, height: 36, borderRadius: '50%',
                      background: r.color, color: 'white', display: 'flex',
                      alignItems: 'center', justifyContent: 'center', fontWeight: 800,
                    }}>{r.value}</span>
                    <div>
                      <div style={{ fontWeight: 700 }}>{r.label}</div>
                      <div className="text-sm text-muted">{r.desc}</div>
                    </div>
                  </div>
                ))}
              </div>

              {error && <div className="alert alert-error">{error}</div>}

              <div style={{ display: 'flex', gap: 12 }}>
                <button className="btn btn-secondary" onClick={startChatAssessment} disabled={chatLoading}>
                  {chatLoading ? 'Starting...' : '💬 Deep Assessment (Chat)'}
                </button>
                <button className="btn btn-primary" style={{ flex: 1 }}
                  onClick={runQuickAssess} disabled={loading || !rating}>
                  {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Assessing...</> : '⚡ Quick Assessment'}
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Chat Assessment */}
      {chatMode && !result && (
        <div className="card">
          <h2 style={{ marginBottom: 16 }}>Conversational Assessment – {domain}</h2>
          <div style={{
            background: '#f8faff', borderRadius: 12, height: 360, overflowY: 'auto',
            padding: 16, display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 16,
          }}>
            {chatMessages.map((msg, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
                <div className={`chat-bubble ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}`}>
                  {msg.content}
                </div>
              </div>
            ))}
            {chatLoading && <div style={{ display: 'flex', gap: 6, padding: '8px 14px' }}>
              <div className="spinner" style={{ width: 16, height: 16 }} />
            </div>}
          </div>
          <div style={{ display: 'flex', gap: 10 }}>
            <input className="form-input" style={{ flex: 1 }}
              placeholder="Type your response..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendChatMessage()}
              disabled={chatLoading} />
            <button className="btn btn-primary" onClick={sendChatMessage} disabled={chatLoading || !chatInput.trim()}>Send</button>
          </div>
        </div>
      )}

      {/* Result */}
      {result && (
        <div>
          <div className="alert alert-success" style={{ marginBottom: 16 }}>
            ✅ Assessment complete for <strong>{result.domain}</strong>!
          </div>
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <h2>Your Assessment Results</h2>
              <span style={{
                padding: '6px 16px', borderRadius: 99, fontWeight: 700,
                background: `${levelColor[result.level]}20`,
                color: levelColor[result.level], fontSize: '0.9rem',
              }}>{result.level?.toUpperCase()}</span>
            </div>

            <div className="grid-2" style={{ marginBottom: 16 }}>
              <div>
                <p className="text-muted text-sm" style={{ marginBottom: 6 }}>Skill Score</p>
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: `${Math.round(result.score * 100)}%` }} />
                </div>
                <p className="text-xs text-muted" style={{ marginTop: 4 }}>{Math.round(result.score * 100)}%</p>
              </div>
              <div>
                <p className="text-muted text-sm">Start With</p>
                <p style={{ fontWeight: 600, marginTop: 4 }}>{result.recommended_start}</p>
              </div>
            </div>

            <div className="grid-2">
              <div>
                <p className="text-muted text-sm" style={{ marginBottom: 6 }}>Strengths</p>
                <ul style={{ paddingLeft: 18 }}>
                  {result.strengths?.map((s, i) => <li key={i} className="text-sm" style={{ marginBottom: 4 }}>✅ {s}</li>)}
                </ul>
              </div>
              <div>
                <p className="text-muted text-sm" style={{ marginBottom: 6 }}>Areas to Improve</p>
                <ul style={{ paddingLeft: 18 }}>
                  {result.gaps?.map((g, i) => <li key={i} className="text-sm" style={{ marginBottom: 4 }}>📚 {g}</li>)}
                </ul>
              </div>
            </div>
          </div>

          <button className="btn btn-secondary" style={{ marginTop: 16 }}
            onClick={() => { setResult(null); setChatMode(false); setDomain(''); setRating(null) }}>
            ← Assess Another Domain
          </button>
        </div>
      )}
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { roadmapAPI } from '../services/api.js'
import StepCard from '../components/StepCard.jsx'

export default function RoadmapView({ studentId }) {
  const { roadmapId } = useParams()
  const [roadmap, setRoadmap] = useState(null)
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [feedback, setFeedback] = useState('')
  const [adapting, setAdapting] = useState(false)
  const [message, setMessage] = useState('')
  const [activeTab, setActiveTab] = useState('steps')

  useEffect(() => {
    loadRoadmap()
  }, [roadmapId])

  const loadRoadmap = async () => {
    try {
      const res = await roadmapAPI.get(roadmapId)
      setRoadmap(res.data)
    } catch (_) {
      setMessage('Failed to load roadmap.')
    } finally {
      setLoading(false)
    }
  }

  const loadReport = async () => {
    try {
      const res = await roadmapAPI.getReport(roadmapId, studentId)
      setReport(res.data)
    } catch (_) {
      setMessage('Failed to load report.')
    }
  }

  const updateProgress = async (stepNumber, pct) => {
    try {
      const res = await roadmapAPI.updateProgress(roadmapId, {
        student_id: studentId,
        step_number: stepNumber,
        completion_percentage: pct,
      })
      // Update local state
      setRoadmap((prev) => ({
        ...prev,
        overall_progress: res.data.overall_progress,
        steps: prev.steps.map((s) =>
          s.step_number === stepNumber
            ? { ...s, completion_percentage: pct, status: pct === 0 ? 'not_started' : pct === 100 ? 'completed' : 'in_progress' }
            : s
        ),
      }))
      if (res.data.ai_feedback) {
        setMessage(res.data.ai_feedback)
      }
    } catch (err) {
      setMessage('Failed to update progress.')
    }
  }

  const adaptRoadmap = async () => {
    if (!feedback.trim()) return
    setAdapting(true)
    try {
      const res = await roadmapAPI.adapt(roadmapId, { student_id: studentId, feedback })
      setRoadmap(res.data.roadmap)
      setFeedback('')
      setMessage('Roadmap adapted based on your feedback!')
    } catch (_) {
      setMessage('Failed to adapt roadmap.')
    } finally {
      setAdapting(false)
    }
  }

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, justifyContent: 'center', minHeight: 300 }}>
      <div className="spinner" /> Loading roadmap...
    </div>
  )

  if (!roadmap) return <div className="alert alert-error">Roadmap not found.</div>

  const completed = roadmap.steps?.filter(s => s.status === 'completed').length || 0

  return (
    <div>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #1e3a8a, #1a6cf6)',
        borderRadius: 16, padding: '24px 28px', color: 'white', marginBottom: 24,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <span style={{ opacity: 0.7, fontSize: '0.85rem' }}>Your Learning Roadmap</span>
            <h1 style={{ fontSize: '1.6rem', marginTop: 4 }}>{roadmap.title}</h1>
            <p style={{ opacity: 0.85, marginTop: 4 }}>Target: {roadmap.target_role} • {roadmap.total_weeks} weeks</p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 900 }}>{roadmap.overall_progress}%</div>
            <div style={{ opacity: 0.8, fontSize: '0.85rem' }}>{completed}/{roadmap.steps?.length} steps</div>
          </div>
        </div>
        <div className="progress-bar" style={{ marginTop: 16, height: 10 }}>
          <div className="progress-fill" style={{ width: `${roadmap.overall_progress}%` }} />
        </div>
      </div>

      {message && (
        <div className="alert alert-info" style={{ marginBottom: 16 }}>
          🤖 {message}
          <button onClick={() => setMessage('')} style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}>✕</button>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: 'white', padding: 4, borderRadius: 10, border: '1px solid #e2e8f0', width: 'fit-content' }}>
        {[['steps', '📋 Steps'], ['report', '📊 Report'], ['adapt', '🔧 Adapt']].map(([tab, label]) => (
          <button key={tab} onClick={() => { setActiveTab(tab); if (tab === 'report' && !report) loadReport() }}
            style={{
              padding: '8px 18px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: activeTab === tab ? '#1a6cf6' : 'transparent',
              color: activeTab === tab ? 'white' : '#64748b',
              fontWeight: 600, fontSize: '0.9rem',
            }}>{label}</button>
        ))}
      </div>

      {/* Steps Tab */}
      {activeTab === 'steps' && (
        <div>
          {roadmap.steps?.map((step) => (
            <StepCard key={step.step_number} step={step} onUpdateProgress={updateProgress} />
          ))}
        </div>
      )}

      {/* Report Tab */}
      {activeTab === 'report' && (
        <div>
          {!report && <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}><div className="spinner" /> Loading weekly report...</div>}
          {report && (
            <div>
              <div className="card" style={{ marginBottom: 16, borderLeft: '4px solid #16a34a' }}>
                <h2 style={{ marginBottom: 8 }}>{report.headline}</h2>
                <p className="text-muted">{report.motivation}</p>
              </div>
              <div className="grid-2" style={{ marginBottom: 16 }}>
                <div className="card">
                  <p className="text-muted text-sm" style={{ marginBottom: 8 }}>Achievements</p>
                  <ul style={{ paddingLeft: 18 }}>
                    {report.achievements?.map((a, i) => (
                      <li key={i} className="text-sm" style={{ marginBottom: 4 }}>✅ {a}</li>
                    ))}
                  </ul>
                </div>
                <div className="card">
                  <p className="text-muted text-sm" style={{ marginBottom: 8 }}>This Week's Focus</p>
                  <p style={{ fontWeight: 600 }}>{report.focus_area}</p>
                  <p className="text-sm text-muted" style={{ marginTop: 8 }}>
                    ~{report.estimated_completion_weeks} weeks to complete
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Adapt Tab */}
      {activeTab === 'adapt' && (
        <div className="card">
          <h2 style={{ marginBottom: 8 }}>Adapt Your Roadmap</h2>
          <p className="text-muted text-sm" style={{ marginBottom: 16 }}>
            Tell IBM Granite AI what's working, what isn't, and how your goals have changed.
          </p>
          <textarea className="form-input"
            rows={4}
            placeholder="e.g. 'I'm struggling with JavaScript, I want to focus more on practical projects' or 'I have less time now, need to reduce pace'"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            style={{ resize: 'vertical', marginBottom: 12 }}
          />
          <button className="btn btn-primary" onClick={adaptRoadmap} disabled={adapting || !feedback.trim()}>
            {adapting ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Adapting with IBM Granite...</> : '🔧 Adapt My Roadmap'}
          </button>
        </div>
      )}

      {/* AI Tips */}
      {roadmap.ai_tips?.length > 0 && activeTab === 'steps' && (
        <div className="card" style={{ marginTop: 24, background: '#fffbeb', borderColor: '#fde68a' }}>
          <p style={{ fontWeight: 700, marginBottom: 8 }}>💡 IBM Granite Tips for You</p>
          <ul style={{ paddingLeft: 20 }}>
            {roadmap.ai_tips.map((tip, i) => (
              <li key={i} className="text-sm" style={{ marginBottom: 6, lineHeight: 1.6 }}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

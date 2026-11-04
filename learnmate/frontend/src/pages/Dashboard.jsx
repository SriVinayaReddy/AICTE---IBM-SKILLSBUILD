import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { studentAPI, roadmapAPI } from '../services/api.js'

export default function Dashboard({ studentId }) {
  const [profile, setProfile] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadData()
  }, [studentId])

  const loadData = async () => {
    try {
      const res = await studentAPI.get(studentId)
      setProfile(res.data)
      if (res.data.current_roadmap_id) {
        const rmRes = await roadmapAPI.get(res.data.current_roadmap_id)
        setRoadmap(rmRes.data)
        // Load recommendation
        try {
          const recRes = await roadmapAPI.getRecommendation(res.data.current_roadmap_id, studentId)
          setRecommendation(recRes.data)
        } catch (_) {}
      }
    } catch (err) {
      setError('Failed to load profile. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const generateRoadmap = async () => {
    setGenerating(true)
    setError('')
    try {
      const res = await roadmapAPI.generate({ student_id: studentId })
      setRoadmap(res.data.roadmap)
      navigate(`/roadmap/${res.data.roadmap_id}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate roadmap.')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: 300, gap: 12 }}>
      <div className="spinner" /> Loading your dashboard...
    </div>
  )

  return (
    <div>
      {/* Hero greeting */}
      <div style={{
        background: 'linear-gradient(135deg, #1a6cf6, #6d28d9)',
        borderRadius: 16, padding: '28px 32px', color: 'white', marginBottom: 24,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        flexWrap: 'wrap', gap: 16,
      }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', marginBottom: 6 }}>
            Welcome back, {profile?.name || 'Learner'}! 👋
          </h1>
          <p style={{ opacity: 0.85, fontSize: '1rem' }}>
            Your AI-powered learning coach is ready to guide you.
          </p>
          <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
            {profile?.interests?.slice(0, 3).map((i) => (
              <span key={i} style={{
                background: 'rgba(255,255,255,0.2)', borderRadius: 99,
                padding: '3px 12px', fontSize: '0.82rem', fontWeight: 600,
              }}>{i}</span>
            ))}
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 900 }}>
            {roadmap?.overall_progress ?? 0}%
          </div>
          <div style={{ opacity: 0.85, fontSize: '0.9rem' }}>Overall Progress</div>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* No roadmap yet */}
      {!roadmap && (
        <div className="card text-center" style={{ padding: 48 }}>
          <div style={{ fontSize: '3rem', marginBottom: 16 }}>🗺️</div>
          <h2 style={{ marginBottom: 8 }}>Ready to build your learning path?</h2>
          <p className="text-muted" style={{ marginBottom: 24, maxWidth: 400, margin: '0 auto 24px' }}>
            Our IBM Granite AI will analyze your interests and create a personalized roadmap just for you.
          </p>
          {profile?.skill_assessments?.length === 0 && (
            <div className="alert alert-info" style={{ maxWidth: 400, margin: '0 auto 16px' }}>
              💡 Complete a <strong>Skill Assessment</strong> first for better roadmap personalization!
            </div>
          )}
          <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="btn btn-secondary" onClick={() => navigate('/assess')}>
              📊 Skill Assessment
            </button>
            <button className="btn btn-primary btn-lg" onClick={generateRoadmap} disabled={generating}>
              {generating ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Generating with IBM Granite...</> : '✨ Generate My Roadmap'}
            </button>
          </div>
        </div>
      )}

      {/* Active roadmap summary */}
      {roadmap && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginBottom: 24 }}>
          <div className="card">
            <p className="text-muted text-sm">Current Roadmap</p>
            <h3 style={{ marginTop: 4 }}>{roadmap.title}</h3>
            <div className="progress-bar" style={{ marginTop: 10 }}>
              <div className="progress-fill" style={{ width: `${roadmap.overall_progress}%` }} />
            </div>
            <p className="text-xs text-muted" style={{ marginTop: 6 }}>{roadmap.overall_progress}% complete</p>
          </div>
          <div className="card">
            <p className="text-muted text-sm">Target Role</p>
            <h3 style={{ marginTop: 4 }}>{roadmap.target_role}</h3>
            <p className="text-sm text-muted" style={{ marginTop: 4 }}>
              {roadmap.steps?.filter(s => s.status === 'completed').length}/{roadmap.steps?.length} steps done
            </p>
          </div>
          <div className="card">
            <p className="text-muted text-sm">Total Duration</p>
            <h3 style={{ marginTop: 4 }}>{roadmap.total_weeks} weeks</h3>
            <p className="text-sm text-muted" style={{ marginTop: 4 }}>
              at {profile?.weekly_hours}h/week
            </p>
          </div>
        </div>
      )}

      {/* AI Recommendation */}
      {recommendation && (
        <div className="card" style={{ borderLeft: '4px solid #1a6cf6', marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p className="text-muted text-xs" style={{ marginBottom: 4 }}>🤖 AI Recommendation</p>
              <p style={{ fontWeight: 600 }}>{recommendation.recommendation}</p>
              <p className="text-sm text-muted" style={{ marginTop: 4 }}>{recommendation.tip}</p>
            </div>
            <span className={`badge badge-${recommendation.priority === 'high' ? 'orange' : 'blue'}`}>
              {recommendation.priority}
            </span>
          </div>
        </div>
      )}

      {/* Action buttons */}
      {roadmap && (
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => navigate(`/roadmap/${roadmap.roadmap_id}`)}>
            📋 View Full Roadmap
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/coach')}>
            💬 Chat with AI Coach
          </button>
          <button className="btn btn-secondary" onClick={generateRoadmap} disabled={generating}>
            {generating ? 'Regenerating...' : '🔄 Regenerate Roadmap'}
          </button>
        </div>
      )}

      {/* AI Summary */}
      {roadmap?.ai_summary && (
        <div className="card" style={{ marginTop: 24, background: '#f8faff' }}>
          <p className="text-muted text-xs" style={{ marginBottom: 6 }}>IBM Granite AI Insight</p>
          <p style={{ lineHeight: 1.7 }}>{roadmap.ai_summary}</p>
          {roadmap.ai_tips?.length > 0 && (
            <ul style={{ marginTop: 12, paddingLeft: 20 }}>
              {roadmap.ai_tips.map((tip, i) => (
                <li key={i} className="text-sm" style={{ marginBottom: 4, color: '#475569' }}>{tip}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}

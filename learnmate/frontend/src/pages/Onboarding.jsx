import { useState } from 'react'
import { studentAPI } from '../services/api.js'

const DOMAINS = [
  'Frontend Development', 'Backend Development', 'Full Stack Development',
  'Data Science & ML', 'Cybersecurity', 'UI/UX Design',
  'Mobile Development', 'Cloud & DevOps',
]

const STYLES = ['visual', 'reading', 'hands-on', 'video', 'mixed']

export default function Onboarding({ onStudentCreated }) {
  const [step, setStep] = useState(1)
  const [form, setForm] = useState({
    name: '', email: '', interests: [], learning_style: 'mixed', weekly_hours: 10,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const toggleInterest = (domain) => {
    setForm((prev) => ({
      ...prev,
      interests: prev.interests.includes(domain)
        ? prev.interests.filter((d) => d !== domain)
        : [...prev.interests, domain],
    }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await studentAPI.create(form)
      onStudentCreated(res.data.student_id)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create profile. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh', background: 'linear-gradient(135deg, #e8f0ff 0%, #f0e8ff 100%)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24,
    }}>
      <div style={{ width: '100%', maxWidth: 560 }}>
        {/* Header */}
        <div className="text-center" style={{ marginBottom: 32 }}>
          <div style={{
            width: 64, height: 64, borderRadius: 18,
            background: 'linear-gradient(135deg, #1a6cf6, #6d28d9)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontWeight: 900, fontSize: '1.8rem', margin: '0 auto 16px',
          }}>L</div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: 8 }}>
            Welcome to <span style={{ color: '#1a6cf6' }}>LearnMate</span>
          </h1>
          <p className="text-muted" style={{ fontSize: '1rem' }}>
            Your Agentic AI coach, powered by IBM Granite
          </p>
        </div>

        {/* Progress indicator */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
          {[1, 2, 3].map((s) => (
            <div key={s} style={{
              flex: 1, height: 4, borderRadius: 99,
              background: s <= step ? '#1a6cf6' : '#e2e8f0', transition: 'background 0.3s',
            }} />
          ))}
        </div>

        <div className="card">
          {step === 1 && (
            <div>
              <h2 style={{ marginBottom: 4 }}>Tell us about yourself</h2>
              <p className="text-muted text-sm" style={{ marginBottom: 20 }}>
                Step 1 of 3 – Basic Information
              </p>
              <div className="form-group">
                <label className="form-label">Your Name *</label>
                <input className="form-input" placeholder="e.g. Priya Sharma"
                  value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Email Address</label>
                <input className="form-input" type="email" placeholder="you@example.com"
                  value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Hours available per week</label>
                <input className="form-input" type="number" min={1} max={80}
                  value={form.weekly_hours}
                  onChange={(e) => setForm({ ...form, weekly_hours: +e.target.value })} />
              </div>
              <button className="btn btn-primary w-full btn-lg"
                disabled={!form.name}
                onClick={() => setStep(2)}>
                Continue →
              </button>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 style={{ marginBottom: 4 }}>What do you want to learn?</h2>
              <p className="text-muted text-sm" style={{ marginBottom: 20 }}>
                Step 2 of 3 – Select your domains of interest
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, marginBottom: 20 }}>
                {DOMAINS.map((domain) => (
                  <span key={domain} className={`chip ${form.interests.includes(domain) ? 'selected' : ''}`}
                    onClick={() => toggleInterest(domain)}>
                    {domain}
                  </span>
                ))}
              </div>
              <div className="form-group">
                <label className="form-label">Learning Style</label>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {STYLES.map((style) => (
                    <span key={style} className={`chip ${form.learning_style === style ? 'selected' : ''}`}
                      onClick={() => setForm({ ...form, learning_style: style })}>
                      {style}
                    </span>
                  ))}
                </div>
              </div>
              <div style={{ display: 'flex', gap: 12, marginTop: 20 }}>
                <button className="btn btn-secondary" onClick={() => setStep(1)}>← Back</button>
                <button className="btn btn-primary" style={{ flex: 1 }}
                  disabled={form.interests.length === 0}
                  onClick={() => setStep(3)}>
                  Continue →
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h2 style={{ marginBottom: 4 }}>Review your profile</h2>
              <p className="text-muted text-sm" style={{ marginBottom: 20 }}>
                Step 3 of 3 – Confirm and create
              </p>
              <div style={{ background: '#f8faff', borderRadius: 10, padding: 16, marginBottom: 20 }}>
                <div style={{ marginBottom: 10 }}>
                  <span className="text-muted text-sm">Name: </span>
                  <strong>{form.name}</strong>
                </div>
                <div style={{ marginBottom: 10 }}>
                  <span className="text-muted text-sm">Weekly hours: </span>
                  <strong>{form.weekly_hours}h</strong>
                </div>
                <div style={{ marginBottom: 10 }}>
                  <span className="text-muted text-sm">Learning style: </span>
                  <strong>{form.learning_style}</strong>
                </div>
                <div>
                  <span className="text-muted text-sm">Interests: </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 6 }}>
                    {form.interests.map((i) => (
                      <span key={i} className="badge badge-blue">{i}</span>
                    ))}
                  </div>
                </div>
              </div>

              {error && <div className="alert alert-error">{error}</div>}

              <div style={{ display: 'flex', gap: 12 }}>
                <button className="btn btn-secondary" onClick={() => setStep(2)}>← Back</button>
                <button className="btn btn-primary btn-lg" style={{ flex: 1 }}
                  onClick={handleSubmit} disabled={loading}>
                  {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Creating...</> : '🚀 Start My Learning Journey'}
                </button>
              </div>
            </div>
          )}
        </div>

        <p className="text-center text-xs text-muted" style={{ marginTop: 16 }}>
          Powered by IBM Granite AI • IBM Cloud Lite
        </p>
      </div>
    </div>
  )
}

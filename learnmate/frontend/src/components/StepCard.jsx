const COLORS = { beginner: '#22c55e', intermediate: '#3b82f6', advanced: '#8b5cf6', expert: '#f59e0b' }

export default function StepCard({ step, index, onUpdateProgress }) {
  const statusColor = {
    not_started: '#94a3b8',
    in_progress: '#3b82f6',
    completed: '#16a34a',
  }[step.status] || '#94a3b8'

  return (
    <div className="card" style={{ marginBottom: 16, borderLeft: `4px solid ${statusColor}` }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
            <span style={{
              width: 28, height: 28, borderRadius: '50%', background: statusColor,
              color: 'white', display: 'inline-flex', alignItems: 'center',
              justifyContent: 'center', fontWeight: 700, fontSize: '0.85rem', flexShrink: 0,
            }}>{step.step_number}</span>
            <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>{step.title}</h3>
            <span className={`badge badge-${step.status === 'completed' ? 'green' : step.status === 'in_progress' ? 'blue' : 'gray'}`}>
              {step.status?.replace('_', ' ')}
            </span>
          </div>
          <p className="text-muted text-sm" style={{ marginLeft: 38, marginBottom: 10 }}>
            {step.description}
          </p>

          {/* Progress bar */}
          <div style={{ marginLeft: 38, marginBottom: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span className="text-xs text-muted">Progress</span>
              <span className="text-xs font-bold" style={{ color: statusColor }}>
                {step.completion_percentage || 0}%
              </span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${step.completion_percentage || 0}%` }} />
            </div>
          </div>

          {/* Skills */}
          {step.skills_gained?.length > 0 && (
            <div style={{ marginLeft: 38, display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }}>
              {step.skills_gained.map((skill) => (
                <span key={skill} className="badge badge-purple">{skill}</span>
              ))}
            </div>
          )}

          {/* Courses */}
          {step.courses?.length > 0 && (
            <div style={{ marginLeft: 38 }}>
              <p className="text-xs text-muted" style={{ marginBottom: 6 }}>Recommended Courses:</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {step.courses.map((course, i) => (
                  <a key={i} href={course.url} target="_blank" rel="noopener noreferrer" style={{
                    display: 'flex', alignItems: 'center', gap: 8, padding: '8px 12px',
                    background: '#f8faff', border: '1px solid #e2e8f0', borderRadius: 8,
                    textDecoration: 'none', color: '#1e293b', transition: 'all 0.15s',
                  }}>
                    <span style={{ flex: 1, fontWeight: 600, fontSize: '0.88rem' }}>{course.title}</span>
                    <span className="badge badge-blue" style={{ fontSize: '0.72rem' }}>{course.provider}</span>
                    {course.is_free && <span className="badge badge-green" style={{ fontSize: '0.72rem' }}>Free</span>}
                    {course.rating > 0 && (
                      <span style={{ fontSize: '0.78rem', color: '#d97706' }}>★ {course.rating}</span>
                    )}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Action buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginLeft: 16, flexShrink: 0 }}>
          <div style={{ display: 'flex', gap: 4 }}>
            {[25, 50, 75, 100].map((pct) => (
              <button key={pct} onClick={() => onUpdateProgress(step.step_number, pct)}
                className="btn btn-sm"
                style={{
                  background: step.completion_percentage >= pct ? '#1a6cf6' : '#f1f5f9',
                  color: step.completion_percentage >= pct ? 'white' : '#64748b',
                  padding: '4px 8px', fontSize: '0.75rem',
                }}>
                {pct}%
              </button>
            ))}
          </div>
          <p className="text-xs text-muted text-center">~{step.estimated_weeks} week{step.estimated_weeks !== 1 ? 's' : ''}</p>
        </div>
      </div>
    </div>
  )
}

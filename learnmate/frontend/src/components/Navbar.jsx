import { Link, useLocation } from 'react-router-dom'

const NAV_LINKS = [
  { to: '/', label: 'Dashboard' },
  { to: '/assess', label: 'Skill Assessment' },
  { to: '/coach', label: 'AI Coach' },
]

export default function Navbar({ studentId, onReset }) {
  const { pathname } = useLocation()

  return (
    <nav style={{
      background: 'white',
      borderBottom: '1px solid #e2e8f0',
      padding: '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: 64,
      position: 'sticky',
      top: 0,
      zIndex: 100,
      boxShadow: '0 2px 12px rgba(26,108,246,0.07)',
    }}>
      {/* Logo */}
      <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 10, textDecoration: 'none' }}>
        <div style={{
          width: 36, height: 36, borderRadius: 10,
          background: 'linear-gradient(135deg, #1a6cf6, #6d28d9)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: 'white', fontWeight: 800, fontSize: '1.1rem',
        }}>L</div>
        <span style={{ fontWeight: 800, fontSize: '1.2rem', color: '#1e293b' }}>
          Learn<span style={{ color: '#1a6cf6' }}>Mate</span>
        </span>
      </Link>

      {/* Nav links */}
      <div style={{ display: 'flex', gap: 4 }}>
        {NAV_LINKS.map(({ to, label }) => (
          <Link key={to} to={to} style={{
            padding: '8px 16px',
            borderRadius: 8,
            textDecoration: 'none',
            fontWeight: 600,
            fontSize: '0.9rem',
            color: pathname === to ? '#1a6cf6' : '#64748b',
            background: pathname === to ? '#e8f0ff' : 'transparent',
            transition: 'all 0.15s',
          }}>{label}</Link>
        ))}
      </div>

      {/* IBM badge + reset */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <span style={{
          padding: '4px 10px', background: '#dbeafe',
          color: '#1d4ed8', borderRadius: 6, fontSize: '0.78rem', fontWeight: 700,
        }}>Powered by IBM Granite</span>
        <button onClick={onReset} style={{
          background: 'none', border: '1.5px solid #e2e8f0',
          borderRadius: 8, padding: '6px 12px', cursor: 'pointer',
          fontSize: '0.82rem', color: '#64748b', fontWeight: 600,
        }}>Sign Out</button>
      </div>
    </nav>
  )
}

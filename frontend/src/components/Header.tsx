import { Link, useNavigate } from 'react-router-dom'
import { useMemo } from 'react'

function Header() {
  const navigate = useNavigate()

  const isLoggedIn = useMemo(() => false, [])

  return (
    <header style={{ width: '100%', borderBottom: '1px solid #e5e5e5', position: 'sticky', top: 0, background: '#fff', zIndex: 10 }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 0' }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#111', fontWeight: 700, fontSize: 18 }}>
          Trading Simulator
        </Link>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {isLoggedIn ? (
            <Link to="/profile" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, textDecoration: 'none', color: '#111' }}>
              <div style={{ width: 28, height: 28, borderRadius: '50%', background: '#ddd' }} />
              <span>Profile</span>
            </Link>
          ) : (
            <button onClick={() => navigate('/login')} style={{ padding: '8px 12px', border: '1px solid #ccc', background: '#fff', borderRadius: 6, cursor: 'pointer' }}>
              Log in
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header



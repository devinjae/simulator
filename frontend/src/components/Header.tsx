import { Link, useNavigate } from 'react-router-dom'
import { useMemo } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import LatencyPill from './LatencyPill'

function Header() {
  const navigate = useNavigate()

  const isLoggedIn = useMemo(() => false, [])

  const { latencyMs, isConnected, isReconnecting } = useWebSocket({
    url: 'ws://localhost:8000/ws/market',
    onMessage: () => {
      // TODO: update price display (FE work)
    },
    pingInterval: 5000, // Ping every 5 seconds
    maxRetries: 0, // TEMP: Only try to connect once (change later in PROD)
    initialBackoff: 500,
    maxBackoff: 10000,
  })

  return (
    <header style={{ width: '100%', borderBottom: '1px solid #e5e5e5', position: 'sticky', top: 0, background: '#fff', zIndex: 10 }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 0' }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#111', fontWeight: 700, fontSize: 18 }}>
          Trading Simulator
        </Link>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <LatencyPill 
            latencyMs={latencyMs} 
            isConnected={isConnected} 
            isReconnecting={isReconnecting} 
          />
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



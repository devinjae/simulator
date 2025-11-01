import { Link, useNavigate } from 'react-router-dom'
import { useMemo } from 'react'
import { useWebSocket } from '../hooks/useWebSocket'
import LatencyPill from './LatencyPill'
import logoUrl from '../assets/logo.png'

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
    <header className="app-header">
      <div className="header-inner">
        <div className="club">
          <Link to="/" className="club-link">
            <img src={logoUrl} alt="" className="club-logo" />
            <span className="club-text">Trading Simulator</span>
          </Link>
        </div>
        <div className="header-actions">
          <LatencyPill
            latencyMs={latencyMs}
            isConnected={isConnected}
            isReconnecting={isReconnecting}
          />
          <Link to="/trades" className="nav-link">Trades</Link>
          {isLoggedIn ? (
            <Link to="/profile" className="btn btn-secondary">Profile</Link>
          ) : (
            <div className="auth-actions">
              <button className="btn btn-outline" onClick={() => navigate('/login?mode=signup')}>Sign Up</button>
              <button className="btn btn-primary" onClick={() => navigate('/login?mode=login')}>Log In</button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header



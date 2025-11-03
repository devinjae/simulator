import { Link, useNavigate } from 'react-router-dom';
import { useMemo } from 'react';
import { useWebSocketContext } from '../contexts/WebSocketContext';
import LatencyPill from './LatencyPill';
import logoUrl from '../assets/logo.png';

function Header() {
  const navigate = useNavigate();
  const { latencyMs, isConnected, isReconnecting } = useWebSocketContext();
  const isLoggedIn = useMemo(() => false, []);

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



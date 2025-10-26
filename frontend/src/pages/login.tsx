import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'

export function Login({ onSwitchTab }: { onSwitchTab: (tab: 'login' | 'register') => void }) {
  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <div>
        <label className="input-label">Username/Email</label>
        <input className="input" type="text" placeholder="Username or Email" />
      </div>
      <div>
        <label className="input-label">Password</label>
        <input className="input" type="password" placeholder="Password" />
      </div>
      <button className="btn btn-primary btn-block">Log in</button>
      <div style={{ fontSize: 14 }}>
        Don't have an account yet?{' '}
        <button onClick={() => onSwitchTab('register')} style={{ background: 'transparent', border: 'none', padding: 0, color: '#892736', cursor: 'pointer' }}>
          Register now
        </button>
      </div>
    </div>
  )
}

export function Register({ onSwitchTab }: { onSwitchTab: (tab: 'login' | 'register') => void }) {
  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <div>
        <label className="input-label">Username</label>
        <input className="input" type="text" placeholder="Username" />
      </div>
      <div>
        <label className="input-label">Email</label>
        <input className="input" type="email" placeholder="Email" />
      </div>
      <div>
        <label className="input-label">Full Name</label>
        <input className="input" type="text" placeholder="Full name" />
      </div>
      <div>
        <label className="input-label">Password</label>
        <input className="input" type="password" placeholder="Password" />
      </div>
      <div>
        <label className="input-label">Confirm Password</label>
        <input className="input" type="password" placeholder="Confirm password" />
      </div>
      <button className="btn btn-primary btn-block">Register</button>
      <div style={{ fontSize: 14 }}>
        Already have an account?{' '}
        <button onClick={() => onSwitchTab('login')} style={{ background: 'transparent', border: 'none', padding: 0, color: '#892736', cursor: 'pointer' }}>
          Log in here
        </button>
      </div>
    </div>
  )
}

function LoginPage() {
  const [tab, setTab] = useState<'login' | 'register'>('login')
  const [searchParams, setSearchParams] = useSearchParams()

  useEffect(() => {
    const mode = searchParams.get('mode')
    if (mode === 'signup' || mode === 'register') {
      setTab('register')
    } else if (mode === 'login') {
      setTab('login')
    }
  }, [searchParams])

  const setTabAndUrl = (next: 'login' | 'register') => {
    setTab(next)
    setSearchParams(next === 'register' ? { mode: 'signup' } : { mode: 'login' })
  }

  return (
    <div className="auth-shell">
      <div className="auth-card">
        {tab === 'login' ? <Login onSwitchTab={setTabAndUrl} /> : <Register onSwitchTab={setTabAndUrl} />}
      </div>
    </div>
  )
}

export default LoginPage



import { useState } from 'react'

export function Login({ onSwitchTab }: { onSwitchTab: (tab: 'login' | 'register') => void }) {
  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Username or Email</label>
        <input className="input" type="text" placeholder="username or email" />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Password</label>
        <input className="input" type="password" placeholder="password" />
      </div>
      <button style={{ padding: '10px 12px', borderRadius: 6, border: '1px solid #ccc', background: '#fff', cursor: 'pointer' }}>Log in</button>
      <div style={{ fontSize: 14 }}>
        Don't have an account yet?{' '}
        <button onClick={() => onSwitchTab('register')} style={{ background: 'transparent', border: 'none', padding: 0, color: '#646cff', cursor: 'pointer' }}>
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
        <label style={{ display: 'block', marginBottom: 4 }}>Username</label>
        <input className="input" type="text" placeholder="username" />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Email</label>
        <input className="input" type="email" placeholder="email" />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Real Name</label>
        <input className="input" type="text" placeholder="real name" />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Password</label>
        <input className="input" type="password" placeholder="password" />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: 4 }}>Confirm Password</label>
        <input className="input" type="password" placeholder="confirm password" />
      </div>
      <button style={{ padding: '10px 12px', borderRadius: 6, border: '1px solid #ccc', background: '#fff', cursor: 'pointer' }}>Register</button>
      <div style={{ fontSize: 14 }}>
        Already have an account?{' '}
        <button onClick={() => onSwitchTab('login')} style={{ background: 'transparent', border: 'none', padding: 0, color: '#646cff', cursor: 'pointer' }}>
          Log in here
        </button>
      </div>
    </div>
  )
}

function LoginPage() {
  const [tab, setTab] = useState<'login' | 'register'>('login')

  return (
    <div className="auth-shell">
      <div className="auth-card">
        {tab === 'login' ? <Login onSwitchTab={setTab} /> : <Register onSwitchTab={setTab} />}
      </div>
    </div>
  )
}

export default LoginPage



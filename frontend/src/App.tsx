import { Routes, Route, Link } from 'react-router-dom'
import Header from './components/Header'
import HomePage from './pages/index'
import TradesPage from './pages/trades'
import LoginPage from './pages/login'
import ProfilePage from './pages/profile'
import './App.css'

function App() {
  return (
    <div>
      <Header />
      <div className="container">
        <nav className="nav-inline">
          <Link to="/">Home</Link>
          <Link to="/trades">Trades</Link>
        </nav>
      </div>
      <main className="main container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/trades" element={<TradesPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/index';
import TradesPage from './pages/trades';
import LoginPage from './pages/login';
import ProfilePage from './pages/profile';
import { AuthProvider } from './contexts/AuthContext';
import { WebSocketProvider } from './contexts/WebSocketContext';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <WebSocketProvider>
        <div>
          <Header />
          <main className="main container">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/trades" element={<TradesPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>
        </div>
      </WebSocketProvider>
    </AuthProvider>
  );
}

export default App;

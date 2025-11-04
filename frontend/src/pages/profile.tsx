import { useAuth } from '../contexts/AuthContext'
import { Navigate } from 'react-router-dom'

function ProfilePage() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div>
      <h1 style={{ margin: '12px 0' }}>Profile</h1>
      {user && (
        <div style={{ display: 'grid', gap: 12 }}>
          <div>
            <strong>Username:</strong> {user.username}
          </div>
          {user.email && (
            <div>
              <strong>Email:</strong> {user.email}
            </div>
          )}
          <div>
            <strong>User ID:</strong> {user.id}
          </div>
          <div>
            <strong>Status:</strong> {user.is_active ? 'Active' : 'Inactive'}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProfilePage



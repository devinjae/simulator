# Authentication System

This document explains how to use the authentication system in the Trading Simulator backend.

## Overview

The authentication system provides:
- Username/password login with JWT tokens
- Password hashing using bcrypt
- Role-based access control (regular users and superusers)
- Unified dependency injection for protecting endpoints

## Architecture

### Folder Structure
```
app/
├── models/          # Database models (SQLModel tables)
├── schemas/         # Pydantic schemas for API validation
├── core/
│   ├── security.py  # Password hashing and JWT utilities
│   └── deps.py      # Authentication dependencies
├── services/
│   └── auth.py      # Authentication business logic
└── api/api_v1/endpoints/
    └── auth.py      # Authentication endpoints
```

### Key Components

1. **User Model** (`app/models/user.py`): Database table definition
2. **User Schemas** (`app/schemas/user.py`): API request/response validation
3. **Security Utils** (`app/core/security.py`): Password hashing and JWT handling
4. **Auth Dependencies** (`app/core/deps.py`): FastAPI dependencies for authentication
5. **Auth Service** (`app/services/auth.py`): Business logic for user operations
6. **Auth Endpoints** (`app/api/api_v1/endpoints/auth.py`): Login/register endpoints

## Usage

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

### 3. Access Protected Endpoints

```bash
curl -X GET "http://localhost:8000/api/v1/trading/portfolio" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 4. Get Current User Info

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Protecting Endpoints

### Basic Authentication (Any logged-in user)

```python
from app.core.deps import get_current_active_user
from app.schemas.user import UserInDB

@router.get("/protected-endpoint")
def protected_endpoint(
    current_user: UserInDB = Depends(get_current_active_user)
):
    return {"message": f"Hello {current_user.username}!"}
```

### Superuser Only

```python
from app.core.deps import get_current_active_superuser

@router.get("/admin-only")
def admin_endpoint(
    current_user: UserInDB = Depends(get_current_active_superuser)
):
    return {"message": "Admin access granted"}
```

### Optional Authentication

```python
from app.core.deps import get_current_user_optional

@router.get("/optional-auth")
def optional_auth_endpoint(
    current_user: Optional[UserInDB] = Depends(get_current_user_optional)
):
    if current_user:
        return {"message": f"Hello {current_user.username}!"}
    else:
        return {"message": "Hello anonymous user!"}
```

## Available Dependencies

- `get_current_user`: Returns authenticated user or raises 401
- `get_current_active_user`: Returns active authenticated user or raises 401/400
- `get_current_active_superuser`: Returns active superuser or raises 401/400/403
- `get_current_user_optional`: Returns authenticated user or None

## Database Migration

To create the users table, run:

```bash
cd backend
python scripts/create_migration.py
alembic upgrade head
```

## Configuration

Authentication settings in `app/core/config.py`:

```python
SECRET_KEY: str = "your-secret-key-change-in-production"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens with configurable expiration
- Role-based access control
- Secure password validation (minimum 8 characters)
- Unique username and email constraints
- Automatic password hashing on user creation/updates

## Example Protected Endpoints

The system includes example protected endpoints:

- `GET /api/v1/trading/portfolio` - Get user's portfolio
- `POST /api/v1/trading/orders` - Create trading order
- `GET /api/v1/trading/orders` - Get user's orders
- `GET /api/v1/users/` - List all users (superuser only)
- `GET /api/v1/users/{user_id}` - Get specific user

## Error Handling

The system provides appropriate HTTP status codes:

- `401 Unauthorized`: Invalid or missing token
- `400 Bad Request`: Inactive user or validation errors
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found
- `422 Unprocessable Entity`: Validation errors

## Testing Authentication

You can test the authentication system using the FastAPI docs at `http://localhost:8000/api/docs`. The docs will show a "Authorize" button where you can enter your JWT token.

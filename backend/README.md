# Trading Simulator Backend

FastAPI-based backend for the web-based stock trading simulator.

## Features

- **RESTful API** for trading operations
- **WebSocket support** for real-time updates
- **PostgreSQL** database with SQLAlchemy ORM
- **JWT authentication**
- **Order matching engine**
- **Real-time portfolio tracking**

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up database:**
   ```bash
   # Start PostgreSQL
   # Update DATABASE_URL in .env
   ```

4. **Run the application:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

5. **Access API documentation:**
   - Swagger UI: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/                 # API routes and endpoints
│   │   └── api_v1/
│   │       ├── endpoints/   # Individual endpoint modules
│   │       └── api.py       # Main API router
│   ├── core/               # Core configuration and utilities
│   ├── db/                 # Database configuration
│   ├── models/             # SQLAlchemy models
│   ├── services/           # Business logic services
│   └── websocket/          # WebSocket handlers
├── tests/                  # Test files
├── migrations/             # Database migrations
├── scripts/                # Utility scripts
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

- **Authentication:** `/api/v1/auth/`
- **Trading Sessions:** `/api/v1/sessions/`
- **Symbols:** `/api/v1/symbols/`
- **Orders:** `/api/v1/orders/`
- **Trades:** `/api/v1/trades/`
- **Portfolio:** `/api/v1/portfolio/`

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`
- Type checking: `mypy .`

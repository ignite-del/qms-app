# QMS (Quality Management System)

A Pharma-compliant Quality Management System built with FastAPI and React, following 21 CFR Part 11 requirements.

## Features

- 🔐 Secure Authentication with OAuth2 + JWT
- 👥 Role-based Access Control (Admin, QA, Analyst)
- 📝 CAPA (Corrective and Preventive Action) Management
- 📄 Document Management with Versioning
- ✍️ Electronic Signatures
- 📊 Audit Trail System
- 🔍 Compliance with 21 CFR Part 11

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Authentication**: OAuth2 with JWT
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd qms-app
   ```

2. Create a `.env` file in the root directory:
   ```env
   # Backend
   DATABASE_URL=postgresql://postgres:postgres@db:5432/qms
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=qms
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development Setup

### Backend

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Project Structure

```
qms-app/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── tests/          # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

For security concerns, please email security@example.com

## Support

For support, please email support@example.com 
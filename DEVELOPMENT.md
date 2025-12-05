# Development Guide

## Quick Start with Docker Compose

The fastest way to get started with local development:

```bash
# Clone the repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python/agentic-workflows

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Access the application
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## Manual Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements-full.txt
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python -c "from agentic_workflows.db.database import init_db; init_db()"

# Run migrations
alembic upgrade head

# Start development server
uvicorn agentic_workflows.api.server:app --reload --port 8000
```

### Frontend Setup

```bash
cd ui

# Install dependencies
npm ci

# Start development server
npm run dev

# Access at http://localhost:3000
```

## Development Workflow

### Running Tests

```bash
# Backend tests
pytest -v --cov=agentic_workflows

# Frontend type check
cd ui && npm run type-check

# Frontend lint
cd ui && npm run lint

# E2E tests
cd ui && npm run test:e2e
```

### Building for Production

```bash
# Build frontend
cd ui && npm run build

# Build Docker image
docker build -t agentic-workflows .

# Run production container
docker run -p 8000:10000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=your-secret-key \
  agentic-workflows
```

## Docker Compose Profiles

### Development Profile (with hot reload)

```bash
docker-compose --profile dev up
```

This starts:
- PostgreSQL
- Redis
- Backend (with volume mounts for hot reload)
- Frontend dev server (with hot reload)

### Production Profile (default)

```bash
docker-compose up
```

This starts:
- PostgreSQL
- Redis
- Backend (serving built frontend)

## Environment Variables

### Required

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT tokens (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Optional

- `REDIS_URL` - Redis connection string (default: redis://localhost:6379/0)
- `SENTRY_DSN` - Sentry DSN for error tracking
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `GITHUB_CLIENT_ID` - GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth client secret

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Connect to PostgreSQL
docker-compose exec postgres psql -U agentic -d agentic_workflows
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

### Frontend Build Issues

```bash
# Clear node_modules and reinstall
cd ui
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

### Backend Import Issues

```bash
# Reinstall in editable mode
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## Database Migrations

### Creating a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Review the generated migration in alembic/versions/

# Apply the migration
alembic upgrade head
```

### Rolling Back Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

## Code Quality

### Pre-commit Checks

```bash
# Run all checks
./scripts/pre-commit.sh

# Or manually:
cd ui && npm run lint && npm run type-check
pytest -v
```

### Code Formatting

```bash
# Python (if black is installed)
black agentic_workflows tests

# TypeScript/JavaScript
cd ui && npm run lint:fix
```

## Performance Profiling

### Backend Profiling

```bash
# Install profiling tools
pip install py-spy

# Profile running application
py-spy top --pid <backend_pid>

# Generate flame graph
py-spy record -o profile.svg --pid <backend_pid>
```

### Frontend Profiling

1. Open Chrome DevTools
2. Go to Performance tab
3. Record interaction
4. Analyze flame graph

## Debugging

### Backend Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use debugpy for VS Code
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

### Frontend Debugging

```typescript
// Use React DevTools browser extension
// Add debugger statement
debugger;

// Console logging
console.log('Debug:', variable);
```

## Common Tasks

### Adding a New API Endpoint

1. Create route in `agentic_workflows/api/routes/`
2. Add tests in `tests/test_api.py`
3. Update API documentation
4. Run tests: `pytest tests/test_api.py`

### Adding a New Frontend Page

1. Create component in `ui/src/pages/`
2. Add route in `ui/src/App.tsx`
3. Add E2E test in `ui/e2e/`
4. Run tests: `npm run test:e2e`

### Adding a New Plugin

1. Create plugin in `agentic_workflows/plugins/`
2. Inherit from `PluginBase`
3. Implement `plan()` and `execute()` methods
4. Register in `plugins/__init__.py`
5. Add tests in `tests/test_plugins.py`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Playwright Documentation](https://playwright.dev/)

## Getting Help

- GitHub Issues: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues
- Email: surajkumarind08@gmail.com

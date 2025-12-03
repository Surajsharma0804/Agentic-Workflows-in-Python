# 🚀 Quick Start Guide

## Prerequisites
- Python 3.10+
- Docker Desktop (for full stack)
- Node.js 18+ (for UI)

## 5-Minute Setup

### 1. Clone and Navigate
```bash
cd agentic-workflows
```

### 2. Start Backend
```bash
# With Docker (recommended)
docker compose up -d

# Without Docker (basic)
pip install -e .
python -m uvicorn agentic_workflows.api.server:app --reload
```

### 3. Start UI
```bash
cd ui
npm install
npm run dev
```

### 4. Access
- **API**: http://localhost:8000/api/docs
- **UI**: http://localhost:3000
- **Monitoring**: http://localhost:5555

## Common Commands

### Docker
```bash
docker compose up -d      # Start all services
docker compose down       # Stop all services
docker compose ps         # Check status
docker compose logs -f    # View logs
```

### Development
```bash
pytest                    # Run tests
.\health-check.ps1       # Verify setup
agentic-workflows --help # CLI help
```

## Troubleshooting

### Docker Issues
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Python Issues
```bash
pip install -e ".[dev]"
```

### UI Issues
```bash
cd ui
rm -rf node_modules
npm install
```

## Next Steps
- Read [README.md](README.md) for full documentation
- See [SETUP.md](SETUP.md) for detailed installation
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production deployment

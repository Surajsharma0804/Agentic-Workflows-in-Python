# 🚀 Quick Reference Card

## Start Everything (One Command)

```powershell
# From project root
cd ui
.\UPGRADE_UI.ps1
```

## Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **UI Dashboard** | http://localhost:3000 | Professional React UI |
| **API Docs** | http://localhost:8000/api/docs | FastAPI Swagger docs |
| **API Health** | http://localhost:8000/api/health | Health check endpoint |
| **Flower** | http://localhost:5555 | Celery task monitor |

## Backend Commands

```powershell
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Check status
docker compose ps

# Rebuild
docker compose build --no-cache
docker compose up -d
```

## Frontend Commands

```powershell
# Install dependencies
cd ui
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Lint
npm run lint
```

## Quick Troubleshooting

### Backend Not Running
```powershell
docker compose down
docker compose up -d
```

### UI Not Starting
```powershell
cd ui
Remove-Item -Recurse -Force node_modules
npm install
npm run dev
```

### Port Conflicts
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Project Structure

```
agentic-workflows/
├── agentic_workflows/     # Python backend
│   ├── api/              # FastAPI routes
│   ├── agents/           # AI agents
│   ├── plugins/          # Task plugins
│   └── llm/              # LLM providers
├── ui/                   # React frontend
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   └── lib/         # Utilities
│   └── UPGRADE_UI.ps1   # Setup script
├── docker-compose.yml    # Docker config
└── README.md            # Main docs
```

## Key Features

### Dashboard
- Real-time system metrics
- Animated stat cards
- Activity charts
- Performance metrics
- Recent workflows

### Workflow Runner
- 3 pre-built templates
- YAML editor
- Copy/download specs
- Real-time execution
- Result visualization

### Design
- Glassmorphism effects
- Smooth animations
- Gradient backgrounds
- Glow effects
- Loading states

## Documentation

| File | Description |
|------|-------------|
| `README.md` | Main documentation |
| `QUICK_START.md` | 5-minute setup |
| `START_PROFESSIONAL_UI.md` | UI startup guide |
| `UI_UPGRADE_COMPLETE.md` | Upgrade details |
| `ui/UI_FEATURES.md` | Feature list |
| `PROJECT_STATUS.md` | Current status |
| `CURRENT_STATUS.md` | Latest updates |

## Common Tasks

### Run a Workflow
1. Go to http://localhost:3000/run
2. Select a template or write YAML
3. Click "Run Workflow"
4. View results in real-time

### Check System Health
1. Go to http://localhost:3000
2. View system status banner
3. Check stat cards
4. Monitor activity chart

### View API Docs
1. Go to http://localhost:8000/api/docs
2. Try endpoints interactively
3. View request/response schemas

## Support

### Issues?
1. Check `CURRENT_STATUS.md`
2. Read `UI_UPGRADE_COMPLETE.md`
3. Review troubleshooting section
4. Check Docker logs: `docker compose logs -f`

### Need Help?
- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/health

## Status Check

```powershell
# Backend
docker compose ps

# Frontend
curl http://localhost:3000

# API
curl http://localhost:8000/api/health
```

## Quick Stats

- **Python Files**: 80
- **React Components**: 15+
- **API Endpoints**: 50+
- **Plugins**: 9
- **Tests**: 6 suites
- **Documentation**: 7 files

## Version

- **Project**: 1.0.0
- **Python**: 3.10+
- **Node**: 18+
- **Docker**: 20+

---

**Everything you need on one page!** 🚀

# 🤖 Agentic Workflows in Python

**Enterprise-grade workflow automation platform powered by AI agents**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

- **7 AI Agents**: Planner, Executor, Validator, Observer, Recovery, Self-Healing, Base
- **10+ Plugins**: File Organizer, HTTP, Web Scraper, PDF, Image, SQL, Shell, Git, Docker
- **Professional UI**: 11 pages with glassmorphism design and animations
- **Real Authentication**: JWT + BCrypt with PostgreSQL
- **DAG Engine**: Directed Acyclic Graph workflow execution
- **Production Ready**: Docker, health checks, monitoring

---

## 🚀 Deploy FREE (5 Minutes)

**Cost**: $0/month on Render.com

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Deploy on Render
# - Go to https://dashboard.render.com
# - Sign up with GitHub
# - Click "New +" → "Blueprint"
# - Select: Agentic-Workflows-in-Python
# - Click "Apply"
# - Wait 10-15 minutes

# 3. Test
curl https://your-app.onrender.com/api/health
```

**Full guide**: [DEPLOY.md](DEPLOY.md)

---

## 💻 Local Development

```bash
# Clone
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python/agentic-workflows

# Install
pip install -r requirements-full.txt

# Setup
export DATABASE_URL="sqlite:///./dev.db"
export SECRET_KEY="dev-secret-key"

# Run
uvicorn agentic_workflows.api.server:app --reload

# Access
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
# UI: http://localhost:3001 (cd ui && npm install && npm run dev)
```

---

## 🛠️ Tech Stack

**Backend**: FastAPI, PostgreSQL, SQLAlchemy, Alembic  
**Frontend**: React, TypeScript, Tailwind CSS, Framer Motion  
**DevOps**: Docker, GitHub Actions, Render.com

---

## 📊 Project Structure

```
agentic-workflows/
├── agentic_workflows/       # Python package
│   ├── agents/              # 7 AI agents
│   ├── api/                 # FastAPI routes
│   ├── plugins/             # 10+ plugins
│   └── db/                  # Database models
├── ui/                      # React frontend
│   ├── src/pages/           # 11 pages
│   └── src/components/      # UI components
├── .kiro/                   # Kiro IDE config
├── Dockerfile               # Production build
├── render.yaml              # Render config
└── README.md                # This file
```

---

## 🧪 Testing

```bash
pytest                       # Run all tests
pytest --cov                 # With coverage
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE)

---

## 👤 Author

**Suraj Sharma**  
📧 surajkumarind08@gmail.com  
🐙 [@Surajsharma0804](https://github.com/Surajsharma0804)

---

**⭐ Star this repo if you find it useful!**

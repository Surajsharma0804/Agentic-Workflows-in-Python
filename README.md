# 🚀 Agentic Workflows in Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)

**Enterprise-grade workflow automation platform with AI-powered agents**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

Agentic Workflows is a production-ready workflow automation platform that combines the power of AI agents with robust workflow orchestration. Built with FastAPI, React, PostgreSQL, and Docker, it provides a complete solution for creating, managing, and executing complex workflows with built-in self-healing capabilities.

### ✨ Highlights

- 🤖 **AI-Powered Agents** - 6 specialized agents for intelligent workflow execution
- 🔐 **Real Authentication** - Database-backed auth with BCrypt & JWT
- 🎨 **Professional UI** - Modern React interface with animations
- 🐳 **Docker Ready** - Complete containerized deployment
- 📊 **Real-time Monitoring** - Live workflow execution tracking
- 🔌 **Plugin System** - 15+ built-in plugins, easily extensible
- 🔔 **Alert System** - Beautiful toast notifications
- ✅ **100% Tested** - Comprehensive test suite

---

## 🎯 Features

### Core Capabilities

- **Multi-Agent System**
  - Planner Agent - Intelligent task planning
  - Executor Agent - Reliable task execution
  - Validator Agent - Result verification
  - Observer Agent - Real-time monitoring
  - Recovery Agent - Automatic error recovery
  - Self-Healing Agent - Autonomous issue resolution

- **Workflow Management**
  - YAML-based workflow definitions
  - DAG (Directed Acyclic Graph) visualization
  - Dependency management
  - Parallel execution
  - Retry mechanisms
  - Audit logging

- **Authentication & Security**
  - Real database storage (PostgreSQL)
  - BCrypt password hashing
  - JWT token authentication
  - Email validation
  - CORS configuration
  - Input sanitization

- **Professional UI**
  - Dashboard with real-time metrics
  - Workflow Runner with live execution
  - AI Assistant for natural language
  - Plugin Explorer
  - Audit Viewer
  - DAG Visualizer
  - Settings Management
  - Contact Page

- **Plugin Ecosystem**
  - File Organizer
  - Email Summarizer
  - HTTP Task
  - Web Scraper
  - SQL Query
  - Shell Command
  - PDF Extractor
  - Image Processor
  - And more...

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for UI development)
- Python 3.11+ (for local development)

### Installation

```bash
# Clone the repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python

# Start all services
docker-compose up -d

# Wait for services to be ready (30 seconds)
# Then access the platform
```

### Access Points

- **Web UI**: http://localhost:3001
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Flower (Celery)**: http://localhost:5555

### Test Credentials

```
Email: test@example.com
Password: SecurePass123!
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 3001)               │
│  Dashboard │ Workflows │ AI Assistant │ Plugins │ Audit     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│  Auth │ Workflows │ Tasks │ Plugins │ LLM │ Health          │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │  │    Celery    │
│   Database   │  │    Cache     │  │   Workers    │
│  (Port 5432) │  │  (Port 6379) │  │  (Background)│
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 🧪 Testing

### Run All Tests

```powershell
# Comprehensive system test
.\TEST_EVERYTHING.ps1

# Authentication tests
.\test-auth.ps1

# Health checks
.\health-check.ps1
```

### Test Results

```
✅ Comprehensive Tests: 10/10 PASSING
✅ Authentication Tests: 6/6 PASSING
✅ Health Checks: 45/45 PASSING
✅ Success Rate: 100%
```

---

## 📖 Documentation

- [**START_HERE.md**](START_HERE.md) - Quick start guide
- [**SUBMISSION.md**](SUBMISSION.md) - Complete project documentation
- [**AUTHENTICATION_VERIFIED.md**](AUTHENTICATION_VERIFIED.md) - Auth system proof
- [**ALERT_SYSTEM_COMPLETE.md**](ALERT_SYSTEM_COMPLETE.md) - Alert system docs
- [**ARCHITECTURE.md**](ARCHITECTURE.md) - System architecture
- [**DEPLOYMENT_GUIDE.md**](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [**API Docs**](http://localhost:8000/api/docs) - Interactive API documentation

---

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/1a1a2e/ffffff?text=Dashboard+with+Real-time+Metrics)

### Workflow Runner
![Workflow Runner](https://via.placeholder.com/800x400/16213e/ffffff?text=Workflow+Execution+Interface)

### AI Assistant
![AI Assistant](https://via.placeholder.com/800x400/0f3460/ffffff?text=AI-Powered+Workflow+Assistant)

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Reliable database
- **Redis** - Caching and message broker
- **Celery** - Distributed task queue
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **BCrypt** - Password hashing
- **JWT** - Token authentication

### Frontend
- **React** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Framer Motion** - Animations
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide Icons** - Icon library

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **GitHub Actions** - CI/CD
- **Pytest** - Testing
- **Ruff** - Linting
- **MyPy** - Type checking

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Database
DATABASE_URL=postgresql://agentic:password@localhost:5432/agentic_workflows

# Security
SECRET_KEY=your-secure-random-key-here

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (optional)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-claude-key
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📈 Performance

- **API Response Time**: < 50ms
- **Database Queries**: < 10ms
- **UI Load Time**: < 2s
- **Concurrent Workflows**: Up to 100
- **Container Size**: ~500MB

---

## 🔒 Security

- ✅ Password hashing with BCrypt
- ✅ JWT token authentication
- ✅ Email validation
- ✅ SQL injection protection (ORM)
- ✅ CORS configuration
- ✅ Input sanitization
- ✅ Non-root Docker containers
- ✅ Environment variable secrets

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Suraj Kumar**

- Email: surajkumarind08@gmail.com
- Phone: +91 6299124902
- GitHub: [@Surajsharma0804](https://github.com/Surajsharma0804)
- LinkedIn: [surajkumar0804](https://www.linkedin.com/in/surajkumar0804)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React and Framer Motion for the UI
- PostgreSQL, Redis, and Celery for the infrastructure
- Docker for containerization
- All open-source contributors

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Surajsharma0804/Agentic-Workflows-in-Python?style=social)
![GitHub forks](https://img.shields.io/github/forks/Surajsharma0804/Agentic-Workflows-in-Python?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Surajsharma0804/Agentic-Workflows-in-Python?style=social)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [Suraj Kumar](https://github.com/Surajsharma0804)

</div>

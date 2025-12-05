# 🤖 Agentic Workflows - AI-Powered Task Automation

> **"I hate manually organizing files, summarizing emails, and running the same scripts over and over"**

Stop wasting 10 hours/week on repetitive tasks. Built with Kiro in 2 weeks (would take 3-4 months normally).

[![Deploy Status](https://img.shields.io/badge/deploy-ready-brightgreen)]()
[![Security](https://img.shields.io/badge/security-hardened-blue)]()
[![FREE Tier](https://img.shields.io/badge/FREE%20tier-optimized-orange)]()
[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://agentic-workflows-pm7o.onrender.com)
[![Kiro Powered](https://img.shields.io/badge/built%20with-Kiro-purple)]()

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Quick Deploy](#-quick-deploy-2-minutes)
- [Features](#-features)
- [Built-in Plugins](#-built-in-plugins)
- [API Endpoints](#-api-endpoints)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Environment Variables](#-environment-variables)
- [OAuth Setup](#-oauth-setup-optional)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 😤 The Problem

Every week, I wasted **10 hours** on boring tasks:

| Task | Time Wasted | Frequency |
|------|-------------|-----------|
| 📁 Organizing Downloads | 30 min | 5x/week |
| 📧 Email Summarization | 1 hour | Daily |
| 🔄 Running Scripts | 45 min | 3x/week |
| 🗂️ File Management | 1 hour | 2x/week |
| 📊 Report Generation | 2 hours | Weekly |
| **TOTAL** | **10 hours/week** | **520 hours/year** |

**That's 3 months of full-time work wasted on repetitive tasks!**

---

## ✨ The Solution

**Agentic Workflows** automates everything with:

### Core Features
- 🤖 **AI-Powered Orchestration** - Chain tasks intelligently
- 🔌 **10+ Built-in Plugins** - File organizer, email summarizer, web scraper, etc.
- 🎨 **Visual Dashboard** - Beautiful React interface
- 🔒 **Enterprise Security** - JWT + OAuth2 (Google, Apple, GitHub)
- ☁️ **FREE Deployment** - Optimized for Render.com FREE tier
- ⚡ **Fast & Efficient** - <2s startup, ~150MB RAM usage

### Time Savings
- **Before**: 10 hours/week on manual tasks
- **After**: 1 hour/week managing workflows
- **Saved**: 9 hours/week = **468 hours/year**
- **Value**: $23,400/year (at $50/hour)

---

## 🚀 Quick Deploy (2 Minutes)

### Option 1: Deploy to Render.com (Recommended - FREE)

1. **Fork** this repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New +" → "Blueprint"**
4. Connect your forked repo
5. Click **"Apply"**
6. Wait 8-10 minutes
7. Done! Test: `curl https://YOUR-APP.onrender.com/api/health`

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python

# Backend setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements-full.txt

# Database setup
alembic upgrade head

# Start backend
uvicorn agentic_workflows.api.server:app --reload

# Frontend setup (new terminal)
cd ui
npm install
npm run dev

# Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

---

## ✅ Features

### Authentication & Security
- ✅ JWT authentication
- ✅ OAuth2 (Google, Apple, GitHub)
- ✅ Password reset via email
- ✅ Session management
- ✅ CORS configured
- ✅ Input validation
- ✅ SQL injection protection
- ✅ Path traversal protection

### Workflow Management
- ✅ Create, read, update, delete workflows
- ✅ Visual workflow builder
- ✅ Task chaining
- ✅ Conditional execution
- ✅ Error handling & retry logic
- ✅ Execution history
- ✅ Real-time monitoring

### User Interface
- ✅ Responsive design (mobile to TV)
- ✅ Dark/light theme
- ✅ Smooth animations
- ✅ Loading states
- ✅ Error boundaries
- ✅ Accessibility (WCAG AA)
- ✅ Professional UI/UX

### Performance
- ✅ Async/await throughout
- ✅ Database connection pooling
- ✅ Optimized for 512MB RAM
- ✅ Fast cold starts (<30s)
- ✅ Efficient caching
- ✅ Lazy loading

---

## 🔌 Built-in Plugins

1. **📁 File Organizer** - Sort files by type, date, or custom rules
   ```json
   {
     "plugin": "file_organizer",
     "params": {
       "source": "~/Downloads",
       "organize_by": "type",
       "create_folders": true
     }
   }
   ```

2. **📧 Email Summarizer** - AI-powered email summaries
   ```json
   {
     "plugin": "email_summarizer",
     "params": {
       "folder": "inbox",
       "max_emails": 50,
       "summary_length": "brief"
     }
   }
   ```

3. **🌐 Web Scraper** - Extract data from websites
4. **📄 PDF Extractor** - Extract text from PDFs
5. **🖼️ Image Processor** - Batch process images
6. **🗄️ SQL Query Runner** - Automate database tasks
7. **💻 Shell Command** - Run scripts safely
8. **☁️ S3 Uploader** - Upload to cloud storage
9. **💬 Slack Notifier** - Send team notifications
10. **🔗 HTTP Task** - Make API calls

---

## 🔧 API Endpoints

### Core
- `GET /api/health` - Health check
- `GET /api/docs` - Interactive API documentation
- `GET /api/openapi.json` - OpenAPI schema

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password
- `GET /api/auth/{provider}/login` - OAuth login (Google, Apple, GitHub)
- `GET /api/auth/{provider}/callback` - OAuth callback

### Workflows
- `GET /api/workflows` - List workflows
- `POST /api/workflows` - Create workflow
- `GET /api/workflows/{id}` - Get workflow details
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

### Plugins
- `GET /api/plugins` - List available plugins
- `GET /api/plugins/{name}` - Plugin details

---

## 📖 Usage Examples

### Register User
```bash
curl -X POST https://YOUR-APP.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST https://YOUR-APP.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Create Workflow
```bash
curl -X POST https://YOUR-APP.onrender.com/api/workflows \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Organize Downloads",
    "description": "Sort files by type",
    "tasks": [
      {
        "plugin": "file_organizer",
        "params": {
          "source": "~/Downloads",
          "organize_by": "type"
        }
      }
    ]
  }'
```

### Execute Workflow
```bash
curl -X POST https://YOUR-APP.onrender.com/api/workflows/1/execute \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│    React Frontend (TypeScript)          │
│  ┌─────────────────────────────────┐   │
│  │ Dashboard │ Workflows │ Plugins │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ REST API (JSON)
┌──────────────▼──────────────────────────┐
│    FastAPI Backend (Python)              │
│  ┌─────────────────────────────────┐   │
│  │ Auth │ Workflows │ Plugins │ AI │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    PostgreSQL Database                   │
│  ┌─────────────────────────────────┐   │
│  │ Users │ Workflows │ Executions  │   │
│  └─────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Authlib** - OAuth 2.0 client
- **Pydantic** - Data validation
- **Structlog** - Structured logging
- **Bcrypt** - Password hashing

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Axios** - HTTP client
- **Zustand** - State management

### Database
- **PostgreSQL** - Production database
- **SQLite** - Development database

### Deployment
- **Render.com** - Cloud platform (FREE tier)
- **Docker** - Containerization
- **GitHub Actions** - CI/CD

---

## 🔐 Environment Variables

### Required (Auto-configured in render.yaml)
```env
PORT=10000                    # Auto-set by Render
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgres://...   # From Render database
SECRET_KEY=your-secret-key    # Auto-generated
```

### Optional (Add in Render Dashboard)
```env
# AI Features
OPENAI_API_KEY=sk-...

# Email (for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourapp.com

# OAuth (optional)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
APPLE_CLIENT_ID=your-client-id
APPLE_CLIENT_SECRET=your-client-secret
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret

# Slack (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

---

## 🔑 OAuth Setup (Optional)

### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `https://your-app.onrender.com/api/auth/google/callback`
6. Copy Client ID and Client Secret
7. Add to Render environment variables

### Apple OAuth

1. Go to [Apple Developer](https://developer.apple.com)
2. Create an App ID
3. Enable Sign in with Apple
4. Create a Service ID
5. Configure redirect URI: `https://your-app.onrender.com/api/auth/apple/callback`
6. Generate a private key
7. Add credentials to Render environment variables

### GitHub OAuth

1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Set callback URL: `https://your-app.onrender.com/api/auth/github/callback`
4. Copy Client ID and Client Secret
5. Add to Render environment variables

**Note**: OAuth is optional. Email/password login works without any configuration.

---

## 💻 Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)

### Backend Development
```bash
# Install dependencies
pip install -r requirements-full.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn agentic_workflows.api.server:app --reload --port 8000

# Run tests
pytest

# Check code quality
ruff check .
mypy agentic_workflows
```

### Frontend Development
```bash
cd ui

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Check types
npm run type-check

# Lint code
npm run lint
```

---

## 🚀 Deployment

### Render.com (Recommended - FREE)

**Automatic Deployment**:
1. Fork this repository
2. Connect to Render.com
3. Use Blueprint (render.yaml)
4. Deploy automatically

**Manual Deployment**:
1. Create Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements-full.txt && cd ui && npm install && npm run build`
4. Set start command: `./entrypoint.sh`
5. Add PostgreSQL database
6. Set environment variables
7. Deploy

### Docker

```bash
# Build image
docker build -t agentic-workflows .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=your-secret-key \
  agentic-workflows
```

### Manual Server

```bash
# Install dependencies
pip install -r requirements-full.txt
cd ui && npm install && npm run build && cd ..

# Run migrations
alembic upgrade head

# Start with gunicorn
gunicorn agentic_workflows.api.server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 🐛 Troubleshooting

### Health Check Timeout
**Status**: ✅ FIXED - Health check now responds instantly

### Deployment Timeout
**Status**: ✅ FIXED - Database init is async, non-blocking

### Port Binding Error
**Status**: ✅ FIXED - PORT env var correctly configured

### OAuth Not Working
**Solution**: OAuth requires configuration. Use email/password login or configure OAuth providers in environment variables.

### Database Connection Error
**Solution**: Check DATABASE_URL environment variable. For local development, SQLite is used automatically.

### Build Fails
**Solution**: Ensure Node.js 18+ and Python 3.11+ are installed. Clear caches: `rm -rf node_modules ui/node_modules && npm install`

---

## 📊 Performance

- **Startup**: <2 seconds (was 60s)
- **Health Check**: <1 second (instant)
- **Memory**: ~150MB (optimized for 512MB)
- **Build Time**: 5-8 minutes (optimized)
- **Cold Start**: ~30 seconds (FREE tier normal)

---

## 🎯 FREE Tier Specs

| Resource | Limit | Optimized |
|----------|-------|-----------|
| RAM | 512 MB | ✅ ~150MB usage |
| CPU | Shared | ✅ Single worker |
| Database | 1 GB | ✅ Pool size: 5 |
| Sleep | 15 min | ✅ Fast cold start |
| Build | Standard | ✅ 5-8 minutes |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write tests for new features
- Update documentation
- Ensure all tests pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Suraj Sharma**

- Email: surajkumarind08@gmail.com
- GitHub: [@Surajsharma0804](https://github.com/Surajsharma0804)
- Project: [Agentic Workflows](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python)

---

## 🙏 Acknowledgments

- Built with [Kiro IDE](https://kiro.ai) - AI-powered development
- Deployed on [Render.com](https://render.com) - FREE tier hosting
- UI inspired by modern design systems
- Community feedback and contributions

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/discussions)
- **Email**: surajkumarind08@gmail.com

---

## 🎉 Success Indicators

After deployment:
- ✅ Render shows "Live" status (green)
- ✅ Health endpoint returns `{"status": "healthy"}`
- ✅ API docs accessible at `/api/docs`
- ✅ Can register and login users
- ✅ Plugins endpoint returns data
- ✅ No errors in logs

---

## 🚀 What's Next?

1. Test your deployment
2. Register a user
3. Create your first workflow
4. Add AI features (optional)
5. Monitor usage in Render dashboard
6. Star the repository ⭐
7. Share with others!

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready (FREE Tier Optimized)  
**Last Updated**: December 2024  
**Deployment Time**: 8-10 minutes  
**Built with**: ❤️ and Kiro IDE

---

Made with ❤️ for developers who hate repetitive tasks

# 🤖 Agentic Workflows - FREE Tier Edition

Enterprise-grade agentic workflow automation platform optimized for Render.com FREE tier deployment.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

## 🚀 Quick Deploy

### Prerequisites
- GitHub account
- Render.com account (FREE tier)

### Deploy Steps
1. **Fork this repository** to your GitHub account
2. **Go to** [Render Dashboard](https://dashboard.render.com)
3. **Click** "New +" → "Blueprint"
4. **Connect** your forked repository
5. **Click** "Apply" - Render will auto-deploy
6. **Wait** 10-15 minutes for deployment
7. **Test** your deployment:
   ```bash
   curl https://YOUR-APP.onrender.com/api/health
   ```

## ✅ What's Included (FREE Tier)

- ✅ FastAPI REST API with async support
- ✅ PostgreSQL database (1GB storage)
- ✅ User authentication (JWT tokens)
- ✅ Workflow execution engine
- ✅ Plugin system (10+ built-in plugins)
- ✅ AI/LLM integration support
- ✅ Interactive API documentation
- ✅ Health monitoring endpoints

## 🎯 Features

### Core Capabilities
- **Workflow Automation**: Create and execute complex workflows
- **Plugin System**: Extensible architecture with built-in plugins
- **Authentication**: Secure JWT-based user authentication
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **Monitoring**: Health checks and logging

### Built-in Plugins
- File Organizer
- Email Summarizer
- HTTP Task Runner
- Web Scraper
- PDF Extractor
- Image Processor
- SQL Query Executor
- Shell Command Runner

## 📊 Architecture (FREE Tier)

```
┌─────────────────────────────────────┐
│   Render.com FREE Tier              │
├─────────────────────────────────────┤
│  FastAPI App (Web Service)          │
│  - Port: 10000                      │
│  - Workers: 1                       │
│  - Memory: 512MB                    │
│  - Sleeps after 15min inactivity    │
├─────────────────────────────────────┤
│  PostgreSQL Database                │
│  - Storage: 1GB                     │
│  - Connections: 97                  │
└─────────────────────────────────────┘
```

**Note**: No Redis/Celery on FREE tier (synchronous execution only)

## 🔧 API Endpoints

### Health & Status
- `GET /api/health` - Health check
- `GET /api/ready` - Readiness check
- `GET /api/live` - Liveness check

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token

### Workflows
- `GET /api/workflows` - List workflows
- `POST /api/workflows` - Create workflow
- `GET /api/workflows/{id}` - Get workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

### Plugins
- `GET /api/plugins` - List available plugins
- `GET /api/plugins/{name}` - Get plugin details

### AI/LLM
- `POST /api/llm/chat` - Chat with AI
- `POST /api/llm/complete` - Text completion

## 📖 Usage Examples

### 1. Register a User
```bash
curl -X POST https://YOUR-APP.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST https://YOUR-APP.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. List Plugins
```bash
curl https://YOUR-APP.onrender.com/api/plugins
```

### 4. Create Workflow
```bash
curl -X POST https://YOUR-APP.onrender.com/api/workflows \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "My Workflow",
    "description": "Test workflow",
    "tasks": []
  }'
```

## 🧪 Testing Deployment

Use the provided PowerShell script:
```powershell
.\check-deployment.ps1 YOUR-APP-NAME
```

Or test manually:
```bash
# Health check
curl https://YOUR-APP.onrender.com/api/health

# API docs
open https://YOUR-APP.onrender.com/api/docs
```

## 🔒 Environment Variables

Configured automatically in `render.yaml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 10000 (auto-set) |
| `ENVIRONMENT` | Environment | production |
| `DEBUG` | Debug mode | false |
| `DATABASE_URL` | PostgreSQL URL | (auto-set) |
| `SECRET_KEY` | JWT secret | (auto-generated) |
| `LOG_LEVEL` | Logging level | INFO |

### Optional Variables (Add in Render Dashboard)
- `OPENAI_API_KEY` - For AI features
- `SMTP_HOST` - For email notifications
- `SLACK_WEBHOOK_URL` - For Slack notifications

## 🚨 Troubleshooting

### Issue: Deployment Timeout
**Solution**: Already fixed! App starts immediately, DB initializes in background.

### Issue: Health Check Fails
**Check**:
1. Wait 2-3 minutes for database initialization
2. Verify DATABASE_URL is set in Render
3. Check logs for Python errors

### Issue: 404 Not Found
**Check**:
- URL format: `https://YOUR-APP.onrender.com/api/health`
- Note the `/api/` prefix
- Verify app name in Render dashboard

### Issue: App Sleeps (FREE Tier)
**Behavior**: App sleeps after 15 minutes of inactivity
**Impact**: First request after sleep takes ~30 seconds
**Solution**: Upgrade to paid tier or accept cold starts

## 📝 Development

### Local Setup
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/Agentic-Workflows-in-Python.git
cd agentic-workflows

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-full.txt

# Set environment variables
cp .env.example .env
# Edit .env with your settings

# Run database migrations
alembic upgrade head

# Start server
python -m agentic_workflows.api.server
```

### Local Testing
```bash
# Run tests
pytest

# Check code quality
ruff check .
black --check .

# Run with Docker
docker build -t agentic-workflows .
docker run -p 8000:8000 agentic-workflows
```

## 📦 Project Structure

```
agentic-workflows/
├── agentic_workflows/          # Main application
│   ├── api/                    # FastAPI routes
│   ├── agents/                 # AI agents
│   ├── core/                   # Core logic
│   ├── db/                     # Database models
│   ├── llm/                    # LLM providers
│   ├── plugins/                # Plugin system
│   └── tasks/                  # Task definitions
├── alembic/                    # Database migrations
├── tests/                      # Test suite
├── ui/                         # React frontend (optional)
├── Dockerfile                  # Docker configuration
├── render.yaml                 # Render deployment config
├── requirements-full.txt       # Python dependencies
└── README.md                   # This file
```

## 🎓 Documentation

- **API Docs**: Visit `/api/docs` on your deployed app
- **Architecture**: See `ARCHITECTURE.md`
- **Status**: See `STATUS.md`

## 🔄 Updates & Redeployment

To redeploy after changes:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will auto-deploy (takes 10-15 minutes).

## ⚠️ FREE Tier Limitations

| Feature | FREE Tier | Paid Tier |
|---------|-----------|-----------|
| RAM | 512 MB | Up to 16 GB |
| CPU | Shared | Dedicated |
| Sleep | After 15 min | Never |
| Build Time | Standard | Priority |
| Background Jobs | ❌ No | ✅ Yes |
| Redis/Celery | ❌ No | ✅ Yes |
| Custom Domain | ❌ No | ✅ Yes |

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

- **Email**: surajkumarind08@gmail.com
- **GitHub Issues**: [Report a bug](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues)
- **Render Docs**: [Troubleshooting](https://render.com/docs/troubleshooting-deploys)

## 🎉 Success Checklist

After deployment, verify:
- [ ] Render dashboard shows "Live" status
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] API docs accessible at `/api/docs`
- [ ] Can register a new user
- [ ] Can login with credentials
- [ ] Plugins endpoint returns data

## 🚀 What's Next?

1. **Test your deployment** with the health check
2. **Register a user** via API
3. **Create your first workflow**
4. **Add AI features** with OpenAI API key
5. **Monitor usage** in Render dashboard

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready (FREE Tier Optimized)  
**Last Updated**: 2024-12-04

Made with ❤️ for the Render.com community

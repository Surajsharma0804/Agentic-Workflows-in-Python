# 🚀 Deployment Guide - Agentic Workflows

Complete deployment guide for multiple platforms.

---

## 📋 Table of Contents

1. [Render.com (FREE)](#rendercom-free)
2. [Google Cloud Run](#google-cloud-run)
3. [AWS ECS](#aws-ecs)
4. [Docker Compose (Self-hosted)](#docker-compose)
5. [Environment Variables](#environment-variables)
6. [Database Setup](#database-setup)
7. [Troubleshooting](#troubleshooting)

---

## 1. Render.com (FREE)

**Cost**: $0/month  
**Time**: 10-15 minutes  
**Best for**: Demos, testing, small projects

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to https://dashboard.render.com
   - Sign up with GitHub
   - Click "New +" → "Blueprint"
   - Select repository: `Agentic-Workflows-in-Python`
   - Click "Apply"
   - Wait 10-15 minutes

3. **Verify Deployment**
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

### Configuration

The `render.yaml` file in the root directory contains all configuration:
- Web service (FREE plan)
- PostgreSQL database (FREE plan)
- Environment variables
- Health checks

### Limitations (FREE Tier)
- App sleeps after 15 min inactivity
- 512MB RAM
- 750 hours/month
- No Redis/Celery

---

## 2. Google Cloud Run

**Cost**: Pay-per-use (~$5-20/month)  
**Time**: 15-20 minutes  
**Best for**: Production, scalability

### Prerequisites
- Google Cloud account
- gcloud CLI installed
- Project created

### Deploy Script

Use the provided script:
```bash
cd deploy/cloud-run
./deploy.sh
```

Or manually:

```bash
# 1. Set project
gcloud config set project YOUR_PROJECT_ID

# 2. Build and push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/agentic-workflows

# 3. Deploy to Cloud Run
gcloud run deploy agentic-workflows \
  --image gcr.io/YOUR_PROJECT_ID/agentic-workflows \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production" \
  --set-env-vars="DATABASE_URL=postgresql://..." \
  --set-env-vars="SECRET_KEY=your-secret-key" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10

# 4. Get URL
gcloud run services describe agentic-workflows \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### Database Setup

**Option 1: Cloud SQL (Recommended)**
```bash
# Create Cloud SQL instance
gcloud sql instances create agentic-workflows-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create agentic_workflows \
  --instance=agentic-workflows-db

# Get connection string
gcloud sql instances describe agentic-workflows-db \
  --format='value(connectionName)'
```

**Option 2: External PostgreSQL**
Use any PostgreSQL provider (ElephantSQL, Supabase, etc.)

---

## 3. AWS ECS

**Cost**: ~$10-30/month  
**Time**: 30-45 minutes  
**Best for**: Enterprise, AWS ecosystem

### Prerequisites
- AWS account
- AWS CLI configured
- ECR repository created

### Deploy Steps

```bash
# 1. Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 2. Build and push image
docker build -t agentic-workflows -f docker/Dockerfile.prod .
docker tag agentic-workflows:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-workflows:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-workflows:latest

# 3. Create ECS task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# 4. Create ECS service
aws ecs create-service \
  --cluster agentic-workflows-cluster \
  --service-name agentic-workflows \
  --task-definition agentic-workflows:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Database Setup

Use AWS RDS PostgreSQL:
```bash
aws rds create-db-instance \
  --db-instance-identifier agentic-workflows-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20
```

---

## 4. Docker Compose (Self-hosted)

**Cost**: Server costs only  
**Time**: 10 minutes  
**Best for**: Self-hosting, full control

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Surajsharma0804/Agentic-Workflows-in-Python.git
cd Agentic-Workflows-in-Python/agentic-workflows

# 2. Create .env file
cp .env.example .env
# Edit .env with your values

# 3. Start services
docker-compose up -d

# 4. Check health
curl http://localhost:8000/api/health
```

### Production Docker Compose

Use `docker/docker-compose.prod.yml`:
```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

---

## 5. Environment Variables

### Required Variables

```bash
# Application
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secret-key-min-32-chars

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# API
PORT=8080
API_HOST=0.0.0.0
```

### Optional Variables

```bash
# Redis (if using Celery)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Monitoring
SENTRY_DSN=https://...
LOG_LEVEL=INFO

# AI Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 6. Database Setup

### Initialize Database

```bash
# Method 1: Automatic (on startup)
# Database tables are created automatically when the app starts

# Method 2: Manual
python -c "from agentic_workflows.db.database import init_db; init_db()"

# Method 3: Alembic migrations
alembic upgrade head
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 7. Troubleshooting

### Common Issues

#### Issue: "Port already in use"
```bash
# Find process using port
lsof -i :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# Kill process
kill -9 PID
```

#### Issue: "Database connection failed"
```bash
# Check database is running
docker ps | grep postgres

# Test connection
psql $DATABASE_URL

# Check logs
docker logs agentic-workflows-db
```

#### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements-full.txt

# Verify installation
python -c "import fastapi; print(fastapi.__version__)"
```

#### Issue: "Health check failing"
```bash
# Check logs
docker logs agentic-workflows-api

# Test health endpoint
curl -v http://localhost:8080/api/health

# Check environment variables
docker exec agentic-workflows-api env | grep DATABASE_URL
```

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Performance Issues

Check resource usage:
```bash
# Docker stats
docker stats

# System resources
htop  # or top
```

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Security audit completed
- [ ] Environment variables configured
- [ ] Database backup created
- [ ] SSL certificate ready
- [ ] Domain configured

### Deployment
- [ ] Build Docker image
- [ ] Push to registry
- [ ] Deploy to platform
- [ ] Run database migrations
- [ ] Verify health checks
- [ ] Test API endpoints

### Post-Deployment
- [ ] Monitor logs
- [ ] Check error rates
- [ ] Verify database connections
- [ ] Test authentication
- [ ] Load test (optional)
- [ ] Setup monitoring alerts

---

## 📞 Support

**Issues**: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues  
**Email**: surajkumarind08@gmail.com  
**Documentation**: See README.md and ARCHITECTURE.md

---

## 🔗 Quick Links

- [Render.com Docs](https://render.com/docs)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [AWS ECS Docs](https://docs.aws.amazon.com/ecs/)
- [Docker Docs](https://docs.docker.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

**Status**: ✅ PRODUCTION READY  
**Last Updated**: 2024-12-04

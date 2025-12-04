# 🚀 Deployment Guide - FREE Tier (Render.com)

**Cost**: $0/month  
**Time**: 10 minutes  
**Status**: Production Ready

---

## Quick Deploy (3 Steps)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://dashboard.render.com
2. Sign up with GitHub (free)
3. Click "New +" → "Blueprint"
4. Select: `Agentic-Workflows-in-Python`
5. Click "Apply"
6. Wait 10-15 minutes

### Step 3: Test
```bash
curl https://your-app.onrender.com/api/health
```

---

## What's Included (FREE)

✅ FastAPI backend  
✅ PostgreSQL database  
✅ 7 AI agents  
✅ 10+ plugins  
✅ Authentication (JWT + BCrypt)  
✅ Professional UI (11 pages)  
✅ SSL certificate  

⚠️ No Redis/Celery (synchronous execution)  
⚠️ App sleeps after 15 min inactivity  
⚠️ 512MB RAM limit  

---

## Troubleshooting

### Build Fails
- Check Render logs
- Verify Dockerfile
- Test locally: `docker build -t test .`

### Health Check Fails
- Wait 2-3 minutes for database
- Check PORT environment variable
- Verify entrypoint.sh is executable

### App Crashes
- Check Render logs for errors
- Verify DATABASE_URL is set
- Check for missing dependencies

---

## Local Development

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
```

---

## Support

**Email**: surajkumarind08@gmail.com  
**GitHub**: @Surajsharma0804  
**Docs**: https://render.com/docs

# 🚀 Deploy to Render.com - Complete Guide

**This is the RECOMMENDED way to share your project with friends!**

Render.com supports Docker, PostgreSQL, Redis, and everything your app needs.

---

## ⚡ Quick Deploy (5 Minutes)

### Option 1: One-Click Deploy with Blueprint

1. **Push render.yaml to GitHub** (already done ✅)

2. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up with GitHub (free)

3. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select repository: `Agentic-Workflows-in-Python`
   - Click "Connect"

4. **Deploy**
   - Render will read `render.yaml`
   - Click "Apply"
   - Wait 5-10 minutes for deployment

5. **Get Your URL**
   ```
   ✅ Your app is live!
   https://agentic-workflows-api.onrender.com
   ```

---

## 📋 Option 2: Manual Setup (10 Minutes)

### Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   ```
   Name: agentic-workflows-db
   Database: agentic_workflows
   User: agentic
   Region: Singapore (or closest to you)
   Plan: Free
   ```
4. Click "Create Database"
5. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Redis Instance

1. Click "New +" → "Redis"
2. Configure:
   ```
   Name: agentic-workflows-redis
   Region: Singapore (same as database)
   Plan: Free
   ```
3. Click "Create Redis"
4. **Copy the Internal Redis URL** (starts with `redis://`)

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Click "Connect account" to link GitHub
3. Select repository: `Agentic-Workflows-in-Python`
4. Click "Connect"

5. Configure:
   ```
   Name: agentic-workflows-api
   Region: Singapore (same as database)
   Branch: main
   Runtime: Docker
   Dockerfile Path: ./Dockerfile
   Docker Context: .
   Plan: Free
   ```

6. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"
   
   ```
   ENVIRONMENT=production
   DEBUG=false
   DATABASE_URL=<paste Internal Database URL from Step 1>
   REDIS_URL=<paste Internal Redis URL from Step 2>
   CELERY_BROKER_URL=<paste Internal Redis URL from Step 2>
   CELERY_RESULT_BACKEND=<paste Internal Redis URL from Step 2>
   SECRET_KEY=<generate with command below>
   LOG_LEVEL=INFO
   ```

   **Generate SECRET_KEY**:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

7. Click "Create Web Service"

### Step 4: Wait for Deployment

- Render will build your Docker image
- This takes 5-10 minutes
- Watch the logs in real-time
- When you see "Deployment live", you're ready!

### Step 5: Test Your App

1. **Get your URL**:
   ```
   https://agentic-workflows-api.onrender.com
   ```

2. **Test API**:
   ```
   https://agentic-workflows-api.onrender.com/api/health
   ```

3. **View API Docs**:
   ```
   https://agentic-workflows-api.onrender.com/api/docs
   ```

---

## 🎨 Deploy Frontend (Optional)

If you want a separate frontend URL:

### Option A: Deploy UI to Vercel

1. **Update API URL in UI**:
   
   Create `ui/.env.production`:
   ```
   VITE_API_URL=https://agentic-workflows-api.onrender.com
   ```

2. **Deploy to Vercel**:
   ```powershell
   cd ui
   npm install -g vercel
   vercel --prod
   ```

3. **Result**:
   - Frontend: `https://agentic-workflows.vercel.app`
   - Backend: `https://agentic-workflows-api.onrender.com`

### Option B: Serve UI from Backend (Simpler)

Your Docker setup already serves the UI from the backend!

Just visit:
```
https://agentic-workflows-api.onrender.com
```

The FastAPI server serves the React UI automatically.

---

## 🔧 Environment Variables Explained

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Sets production mode |
| `DEBUG` | `false` | Disables debug mode |
| `DATABASE_URL` | From Render | PostgreSQL connection |
| `REDIS_URL` | From Render | Redis connection |
| `CELERY_BROKER_URL` | Same as Redis | Celery message broker |
| `CELERY_RESULT_BACKEND` | Same as Redis | Celery results storage |
| `SECRET_KEY` | Random string | JWT signing key |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 📊 What Gets Deployed

Your Render deployment includes:

✅ **FastAPI Backend**
- All API routes
- Authentication system
- Workflow engine
- AI agents

✅ **PostgreSQL Database**
- User accounts
- Workflow data
- Audit logs
- Persistent storage

✅ **Redis Cache**
- Session storage
- Task queue
- Real-time data

✅ **React UI**
- Professional interface
- All 8 pages
- Animations
- Responsive design

✅ **Celery Workers** (if configured)
- Background tasks
- Scheduled jobs
- Async processing

---

## 🎯 Share with Friends

Once deployed, share:

```
🎉 Check out my Agentic Workflows project!

🌐 Live Demo: https://agentic-workflows-api.onrender.com
📚 API Docs: https://agentic-workflows-api.onrender.com/api/docs
💻 GitHub: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python

Try it out:
1. Visit the URL
2. Click "Register" to create account
3. Login and explore!

Features:
✨ AI-powered workflow automation
🤖 Multiple AI agents
📊 Real-time dashboard
🔐 Secure authentication
🎨 Beautiful UI with animations
```

---

## 🚨 Troubleshooting

### Build Fails

**Check Dockerfile**:
```powershell
# Test locally first
docker build -t agentic-workflows .
docker run -p 8000:8000 agentic-workflows
```

**Common Issues**:
- Missing dependencies → Check `requirements.txt`
- Port conflicts → Render uses PORT env var
- Build timeout → Optimize Dockerfile

### Database Connection Fails

**Check Environment Variables**:
- Ensure `DATABASE_URL` is set correctly
- Use **Internal Database URL** (not External)
- Format: `postgresql://user:pass@host:5432/dbname`

**Test Connection**:
```python
# In Render shell
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print(engine.connect())"
```

### App Crashes on Startup

**Check Logs**:
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. Look for error messages

**Common Fixes**:
- Missing env vars → Add them in Settings
- Database not ready → Add health checks
- Port binding → Use `0.0.0.0:$PORT`

### Slow Performance

**Free Tier Limitations**:
- Spins down after 15 min inactivity
- First request takes 30-60 seconds
- Limited CPU/memory

**Solutions**:
- Upgrade to paid plan ($7/month)
- Use cron job to keep alive
- Accept cold starts for free tier

---

## 💰 Pricing

### Free Tier (Perfect for Sharing)
- ✅ 750 hours/month
- ✅ PostgreSQL database
- ✅ Redis instance
- ✅ SSL certificate
- ✅ Auto-deploy from GitHub
- ⚠️ Spins down after 15 min
- ⚠️ 512 MB RAM

### Starter Plan ($7/month)
- ✅ Always on
- ✅ 1 GB RAM
- ✅ Faster builds
- ✅ No spin down

**Recommendation**: Start with free tier for sharing with friends!

---

## 🔄 Auto-Deploy from GitHub

Render automatically deploys when you push to GitHub!

```powershell
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Render automatically:
# 1. Detects push
# 2. Builds new Docker image
# 3. Deploys to production
# 4. Zero downtime!
```

---

## 📱 Mobile Access

Your app works on mobile!

- Responsive design ✅
- Touch-friendly ✅
- Fast loading ✅

Share the URL with friends on their phones!

---

## 🎓 Next Steps

### After Deployment:

1. **Test Everything**:
   - Register new account
   - Login
   - Run a workflow
   - Check dashboard
   - Test all features

2. **Monitor**:
   - Check Render logs
   - Monitor database usage
   - Watch for errors

3. **Share**:
   - Send URL to friends
   - Post on social media
   - Add to portfolio

4. **Improve**:
   - Add more features
   - Optimize performance
   - Collect feedback

---

## 📞 Support

**Render Issues**:
- Docs: https://render.com/docs
- Community: https://community.render.com
- Support: support@render.com

**Project Issues**:
- Email: surajkumarind08@gmail.com
- GitHub: @Surajsharma0804
- LinkedIn: linkedin.com/in/surajkumar0804

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Code pushed to GitHub
- [ ] `.kiro` directory included
- [ ] Repository is PUBLIC
- [ ] Docker builds locally
- [ ] Tests passing

During deployment:
- [ ] PostgreSQL created
- [ ] Redis created
- [ ] Web service created
- [ ] Environment variables set
- [ ] Build successful

After deployment:
- [ ] Health check passes
- [ ] Can register account
- [ ] Can login
- [ ] Features work
- [ ] Shared with friends!

---

## 🎉 You're Ready!

**Render.com is the perfect platform for your full-stack app.**

Unlike Vercel:
- ✅ Supports Docker
- ✅ Includes PostgreSQL
- ✅ Includes Redis
- ✅ No 10-second timeout
- ✅ Background workers
- ✅ Free tier available

**Deploy now and share with friends!** 🚀


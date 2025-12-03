# 🚀 Vercel Deployment Guide

## ⚠️ Important Note

Your application has **two parts**:
1. **Frontend (React UI)** - Can be deployed to Vercel ✅
2. **Backend (FastAPI + PostgreSQL + Redis)** - Cannot be deployed to Vercel ❌

**Vercel is designed for frontend applications and serverless functions, not full-stack apps with databases.**

---

## 🎯 Recommended Deployment Strategy

### Option 1: Split Deployment (Recommended)

**Frontend on Vercel + Backend on Render/Railway**

#### Step 1: Deploy Backend to Render.com (Free)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   ```
   Name: agentic-workflows-api
   Environment: Docker
   Region: Choose closest to you
   Branch: main
   Dockerfile Path: ./Dockerfile
   ```
6. Add Environment Variables:
   ```
   DATABASE_URL=<provided by Render PostgreSQL>
   REDIS_URL=<provided by Render Redis>
   SECRET_KEY=<generate secure key>
   ENVIRONMENT=production
   ```
7. Click "Create Web Service"
8. Note your API URL: `https://agentic-workflows-api.onrender.com`

#### Step 2: Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New" → "Project"
4. Import your repository
5. Configure:
   ```
   Framework Preset: Vite
   Root Directory: ui
   Build Command: npm run build
   Output Directory: dist
   ```
6. Add Environment Variable:
   ```
   VITE_API_URL=https://agentic-workflows-api.onrender.com
   ```
7. Click "Deploy"

#### Step 3: Update Frontend to Use API URL

Update `ui/src/contexts/AuthContext.tsx` and other API calls:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Use API_URL in all fetch calls
const response = await fetch(`${API_URL}/api/auth/login`, {
  method: 'POST',
  // ...
})
```

---

### Option 2: All-in-One Deployment

**Deploy Everything to Render.com or Railway.app**

Both services support Docker and databases.

#### Render.com (Recommended - Free Tier Available)

1. Create account at https://render.com
2. Create PostgreSQL database (free tier)
3. Create Redis instance (free tier)
4. Create Web Service from Docker
5. Deploy!

**Advantages:**
- ✅ Free tier available
- ✅ Supports Docker
- ✅ Includes PostgreSQL & Redis
- ✅ Auto-deploys from GitHub
- ✅ SSL certificates included

#### Railway.app (Alternative)

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add PostgreSQL and Redis from marketplace
5. Deploy!

**Advantages:**
- ✅ Very easy setup
- ✅ Great developer experience
- ✅ Automatic environment variables
- ✅ Built-in monitoring

---

### Option 3: Frontend-Only Demo on Vercel

**Deploy just the UI with mock data for demonstration**

This is good for showing your friends the UI without backend functionality.

#### Quick Setup:

1. Create `ui/.env.production`:
   ```
   VITE_API_URL=https://demo-api.example.com
   VITE_DEMO_MODE=true
   ```

2. Update `ui/src/contexts/AuthContext.tsx` to use mock data in demo mode:
   ```typescript
   const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === 'true'
   
   if (DEMO_MODE) {
     // Use mock authentication
     return mockLogin(email, password)
   }
   ```

3. Deploy to Vercel:
   ```bash
   cd ui
   vercel
   ```

---

## 🚀 Quick Deploy to Vercel (Frontend Only)

### Step-by-Step:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Navigate to UI directory**:
   ```bash
   cd ui
   ```

3. **Build the project**:
   ```bash
   npm install
   npm run build
   ```

4. **Deploy**:
   ```bash
   vercel
   ```

5. **Follow prompts**:
   - Set up and deploy? **Y**
   - Which scope? **Your account**
   - Link to existing project? **N**
   - Project name? **agentic-workflows**
   - Directory? **./dist**
   - Override settings? **N**

6. **Get your URL**:
   ```
   ✅ Deployed to: https://agentic-workflows-xyz.vercel.app
   ```

---

## 📝 Vercel Configuration for UI Only

Create `ui/vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 🔧 Environment Variables for Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```
VITE_API_URL=https://your-backend-url.onrender.com
VITE_APP_NAME=Agentic Workflows
VITE_ENVIRONMENT=production
```

---

## ⚠️ Why Full Stack Doesn't Work on Vercel

Vercel limitations:
- ❌ No persistent storage (database)
- ❌ No long-running processes (Celery workers)
- ❌ No Redis/PostgreSQL hosting
- ❌ 10-second function timeout
- ❌ Limited memory (1GB)

Your app needs:
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Celery workers
- ✅ Long-running processes
- ✅ Persistent storage

**Solution**: Use Render.com or Railway.app for full deployment

---

## 🎯 Recommended: Deploy to Render.com

**This is the easiest way to share with friends!**

### One-Click Deploy:

1. Push your code to GitHub (already done ✅)
2. Go to https://render.com
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will detect `docker-compose.yml` and deploy everything!

**Result**: You get a URL like `https://agentic-workflows.onrender.com`

**Free tier includes**:
- Web service
- PostgreSQL database
- Redis instance
- SSL certificate
- Auto-deploy from GitHub

---

## 📱 Share with Friends

Once deployed, share:
- **Frontend URL**: `https://your-app.vercel.app` (if UI only)
- **Full App URL**: `https://your-app.onrender.com` (if Render)
- **API Docs**: `https://your-app.onrender.com/api/docs`

**Test Credentials**:
```
Email: demo@example.com
Password: Demo123!
```

---

## 🆘 Need Help?

**For Vercel Issues**:
- Check build logs in Vercel dashboard
- Ensure `ui/dist` directory exists
- Verify `package.json` has correct build script

**For Render Issues**:
- Check deployment logs
- Verify environment variables
- Ensure Docker builds locally first

**Contact**:
- Email: surajkumarind08@gmail.com
- GitHub: @Surajsharma0804

---

## 🎉 Quick Summary

**Best Options**:

1. **For Demo (UI Only)**: Vercel ✅
   - Fast deployment
   - Free
   - Great for showing UI
   - No backend functionality

2. **For Full App**: Render.com ✅
   - Everything works
   - Free tier available
   - Easy setup
   - Shareable URL

3. **Alternative**: Railway.app ✅
   - Similar to Render
   - Great UX
   - Easy deployment

**Choose based on your needs!**

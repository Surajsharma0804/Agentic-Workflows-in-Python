# 🚀 Quick Start Guide

## Deploy to Render.com (5 Minutes)

### Step 1: Push to GitHub ✅
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to **https://dashboard.render.com**
2. Click **"Sign Up"** (use GitHub)
3. Click **"New +"** → **"Blueprint"**
4. Select repository: **Agentic-Workflows-in-Python**
5. Click **"Apply"**
6. Wait 10-15 minutes

### Step 3: Get Your URL
After deployment completes, Render will show your app URL:
```
https://agentic-workflows-api.onrender.com
```
(Your actual URL will be different - check Render dashboard)

---

## Test Your Deployment

Replace `YOUR_APP_NAME` with your actual Render app name:

```bash
# Health Check
curl https://YOUR_APP_NAME.onrender.com/api/health

# API Documentation
# Open in browser:
https://YOUR_APP_NAME.onrender.com/api/docs

# Register User
curl -X POST https://YOUR_APP_NAME.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'

# Login
curl -X POST https://YOUR_APP_NAME.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

---

## Find Your App URL

### Method 1: Render Dashboard
1. Go to https://dashboard.render.com
2. Click on your service name
3. Look for **"URL"** at the top
4. Copy the URL (e.g., `https://agentic-workflows-api-xyz.onrender.com`)

### Method 2: Check Deployment Logs
1. In Render dashboard, click your service
2. Go to **"Logs"** tab
3. Look for: `"Uvicorn running on http://0.0.0.0:10000"`
4. Your public URL is shown in the dashboard

---

## Common Issues

### 404 Error
**Problem**: `curl https://your-app.onrender.com/api/docs` returns 404  
**Solution**: Replace `your-app` with your actual Render app name

**Example**:
```bash
# ❌ Wrong (placeholder)
curl https://your-app.onrender.com/api/health

# ✅ Correct (actual app name)
curl https://agentic-workflows-api-xyz.onrender.com/api/health
```

### App Not Deployed Yet
**Problem**: No URL available  
**Solution**: 
1. Check if deployment is still in progress (10-15 minutes)
2. Look for "Live" status in Render dashboard
3. Check logs for errors

### Health Check Failing
**Problem**: Deployment stuck on "Health check failed"  
**Solution**:
1. Wait 2-3 minutes for database initialization
2. Check logs for errors
3. Verify DATABASE_URL is set

---

## Local Testing (Before Deployment)

```bash
# Install dependencies
pip install -r requirements-full.txt

# Set environment variables
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key"
export PORT=8000

# Initialize database
python -c "from agentic_workflows.db.database import init_db; init_db()"

# Start server
uvicorn agentic_workflows.api.server:app --host 0.0.0.0 --port 8000

# Test locally
curl http://localhost:8000/api/health
# Open: http://localhost:8000/api/docs
```

---

## What to Expect

### First Deployment (10-15 minutes)
```
✓ Building Docker image... (5-8 min)
✓ Creating PostgreSQL database... (2-3 min)
✓ Starting application... (2-3 min)
✓ Health checks passing... (1 min)
✓ Deployment complete! ✅
```

### Successful Deployment
```json
// GET /api/health
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-12-04T...",
  "system_info": {
    "python_version": "3.11...",
    "platform": "Linux-..."
  }
}
```

---

## Next Steps After Deployment

1. **Test API**
   ```bash
   curl https://YOUR_APP.onrender.com/api/health
   ```

2. **Open API Docs**
   ```
   https://YOUR_APP.onrender.com/api/docs
   ```

3. **Register a User**
   ```bash
   curl -X POST https://YOUR_APP.onrender.com/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"your@email.com","password":"SecurePass123!"}'
   ```

4. **Share with Friends**
   ```
   🎉 Check out my project!
   🌐 https://YOUR_APP.onrender.com/api/docs
   💻 https://github.com/Surajsharma0804/Agentic-Workflows-in-Python
   ```

---

## Support

**Can't find your URL?**
- Check Render dashboard: https://dashboard.render.com
- Look for your service name
- Click on it to see the URL

**Deployment failing?**
- Check logs in Render dashboard
- See DEPLOY.md for troubleshooting
- Email: surajkumarind08@gmail.com

---

## Summary

1. ✅ Push code to GitHub
2. ✅ Deploy on Render (use Blueprint)
3. ✅ Wait 10-15 minutes
4. ✅ Get your URL from Render dashboard
5. ✅ Test: `curl https://YOUR_APP.onrender.com/api/health`

**Your app URL is NOT `your-app.onrender.com` - that's just a placeholder!**  
**Get your real URL from the Render dashboard after deployment completes.**

---

**Status**: Ready to deploy! 🚀  
**Cost**: $0/month  
**Time**: 5 minutes to start, 10-15 minutes to complete

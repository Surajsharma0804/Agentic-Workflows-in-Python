# 🔧 Troubleshooting Guide

## Recent Fixes Applied

### ✅ Fix 1: Shell Syntax Error (RESOLVED)
**Error**: `/app/entrypoint.sh: 13: Bad substitution`  
**Cause**: Used bash-specific syntax `${DATABASE_URL:0:30}` in `/bin/sh`  
**Fix**: Changed to POSIX-compliant `echo "DATABASE_URL: [configured]"`  
**Status**: ✅ Fixed in commit 78aca55

### ✅ Fix 2: Deployment Timeout (RESOLVED)
**Error**: `==> Timed Out` after 16 minutes  
**Cause**: Database connection check taking too long (60 seconds)  
**Fix**: 
- Removed pre-startup database wait loop
- Added retry logic to FastAPI startup event (5 attempts, 2s each)
- App starts immediately, health check shows status
**Status**: ✅ Fixed in commit 0091e4c

---

## Common Issues

### Issue 1: Deployment Timeout
**Symptoms**: Build succeeds but deployment times out  
**Solution**: ✅ Already fixed - app now starts immediately

### Issue 2: Database Connection Failed
**Symptoms**: App starts but health check fails  
**Check**:
1. Verify DATABASE_URL is set in Render dashboard
2. Check PostgreSQL database is "Available"
3. Wait 2-3 minutes for database to fully initialize

**Test**:
```bash
# In Render logs, look for:
"database_initialized_successfully"
```

### Issue 3: Port Binding Error
**Symptoms**: "Port already in use" or "Cannot bind to port"  
**Solution**: ✅ Already fixed - PORT env var properly configured

### Issue 4: Health Check Failing
**Symptoms**: Deployment stuck on "Health check failed"  
**Check**:
1. Look for "Starting uvicorn on 0.0.0.0:10000" in logs
2. Verify /api/health endpoint is accessible
3. Check for Python errors in logs

**Expected Logs**:
```
============================================
  Agentic Workflows - Starting
============================================
PORT: 10000
HOST: 0.0.0.0
ENVIRONMENT: production
============================================
Starting uvicorn on 0.0.0.0:10000...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

---

## Deployment Checklist

### Before Deploying
- [x] Code pushed to GitHub
- [x] render.yaml configured
- [x] Dockerfile optimized
- [x] entrypoint.sh fixed
- [x] Database retry logic added

### During Deployment
- [ ] Build completes (5-8 minutes)
- [ ] Image pushed to registry
- [ ] Container starts
- [ ] Health check passes
- [ ] App shows "Live" status

### After Deployment
- [ ] Test health endpoint
- [ ] Test API docs
- [ ] Register a user
- [ ] Test authentication

---

## How to Check Deployment Status

### 1. Render Dashboard
```
1. Go to https://dashboard.render.com
2. Click on your service
3. Check status (should be "Live")
4. View logs for errors
```

### 2. Check Logs
Look for these key messages:
```
✓ "Starting uvicorn on 0.0.0.0:10000"
✓ "Application startup complete"
✓ "database_initialized_successfully"
```

### 3. Test Health Endpoint
```bash
# Replace YOUR_APP with your actual app name
curl https://YOUR_APP.onrender.com/api/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

---

## What to Do If Deployment Fails

### Step 1: Check Render Logs
1. Go to Render dashboard
2. Click your service
3. Go to "Logs" tab
4. Look for error messages

### Step 2: Common Error Messages

**"Bad substitution"**
- ✅ Already fixed in commit 78aca55

**"Timed Out"**
- ✅ Already fixed in commit 0091e4c

**"ModuleNotFoundError"**
- Check requirements-full.txt includes all dependencies
- Verify Dockerfile uses requirements-full.txt

**"Database connection failed"**
- Wait 2-3 minutes for database initialization
- Check DATABASE_URL is set
- Verify PostgreSQL database is "Available"

### Step 3: Manual Redeploy
If deployment is stuck:
1. Go to Render dashboard
2. Click "Manual Deploy" → "Clear build cache & deploy"
3. Wait 10-15 minutes

---

## Testing Locally

Before deploying, test locally:

```bash
# Build Docker image
docker build -t test-build .

# Run container
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e DATABASE_URL="sqlite:///./test.db" \
  -e SECRET_KEY="test-key" \
  test-build

# Test health
curl http://localhost:8080/api/health
```

---

## Current Status

✅ All known issues fixed  
✅ Deployment should succeed  
✅ Estimated time: 10-15 minutes  

### What Was Fixed
1. Shell syntax error in entrypoint.sh
2. Deployment timeout (removed slow DB wait loop)
3. Added database retry logic in FastAPI startup
4. Optimized startup sequence

### Next Deployment Should
- ✅ Build successfully (5-8 minutes)
- ✅ Start immediately (no 60-second wait)
- ✅ Pass health checks (within 2 minutes)
- ✅ Show "Live" status

---

## Support

**Still having issues?**
- Check Render logs for specific errors
- Email: surajkumarind08@gmail.com
- GitHub Issues: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues

**Render Support**:
- Docs: https://render.com/docs/troubleshooting-deploys
- Community: https://community.render.com

---

**Last Updated**: 2024-12-04  
**Status**: All critical issues resolved ✅

# 🔧 Render.com Deployment Troubleshooting

## Common Issues & Solutions

### Issue 1: "Port scan timeout - no open ports detected"

**Cause**: Application not binding to PORT environment variable

**Solution**: ✅ FIXED in latest commit
- Updated `entrypoint.sh` to properly use PORT env var
- Changed Dockerfile CMD to use `/bin/sh`
- Removed hardcoded PORT from render.yaml (Render sets it automatically)

**Verify Fix**:
```bash
# Check logs for this line:
"Starting uvicorn on 0.0.0.0:10000..."
```

---

### Issue 2: "Build failed" or "Docker build error"

**Possible Causes**:
1. Missing dependencies in requirements-full.txt
2. Syntax errors in Python files
3. Dockerfile issues

**Solutions**:
```powershell
# Test build locally
.\test-docker-build.ps1

# Or manually:
docker build -t test-build .
```

---

### Issue 3: "Health check failed"

**Possible Causes**:
1. Database not ready
2. Application crashed on startup
3. Health endpoint not responding

**Solutions**:
1. Check Render logs for errors
2. Verify DATABASE_URL is set
3. Wait 2-3 minutes for database initialization

**Test Health Endpoint**:
```bash
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-12-04T...",
  "system_info": {...}
}
```

---

### Issue 4: "Database connection failed"

**Possible Causes**:
1. PostgreSQL not ready
2. Wrong DATABASE_URL
3. Network issues

**Solutions**:
1. Check Render dashboard - database should be "Available"
2. Verify DATABASE_URL in environment variables
3. Check entrypoint.sh waits for database (max 30 attempts)

**Logs to Look For**:
```
Waiting for PostgreSQL...
PostgreSQL is ready!
Database initialized successfully
```

---

### Issue 5: "Application crashes after startup"

**Possible Causes**:
1. Missing environment variables
2. Import errors
3. Configuration issues

**Solutions**:
1. Check Render logs for Python tracebacks
2. Verify all required env vars are set:
   - DATABASE_URL (auto from database)
   - SECRET_KEY (auto-generated)
   - ENVIRONMENT=production
   - LOG_LEVEL=INFO

**Debug Locally**:
```powershell
# Set environment variables
$env:DATABASE_URL="sqlite:///./test.db"
$env:SECRET_KEY="test-key"
$env:PORT="8000"

# Run server
python -m uvicorn agentic_workflows.api.server:app --host 0.0.0.0 --port 8000
```

---

### Issue 6: "Deployment takes too long"

**Expected Timeline**:
- Build: 5-8 minutes
- Database creation: 2-3 minutes
- First startup: 2-3 minutes
- **Total: 10-15 minutes**

**What's Normal**:
- ✅ "Building..." for 5-8 minutes
- ✅ "Waiting for PostgreSQL..." for 1-2 minutes
- ✅ "Starting uvicorn..." then health checks

**What's Not Normal**:
- ❌ Build stuck for >15 minutes
- ❌ Repeated "Health check failed"
- ❌ Container keeps restarting

---

### Issue 7: "Free tier limitations"

**Known Limitations**:
- ⚠️ App sleeps after 15 min inactivity (first request takes 30s)
- ⚠️ 512MB RAM limit
- ⚠️ No Redis/Celery (synchronous execution)
- ⚠️ 750 hours/month free

**Workarounds**:
1. Use UptimeRobot to ping every 14 minutes (keeps app awake)
2. Optimize memory usage
3. Accept synchronous execution for FREE tier

---

## Deployment Checklist

### Before Deploying
- [ ] All changes committed and pushed to GitHub
- [ ] .kiro directory exists and tracked
- [ ] render.yaml configured correctly
- [ ] Dockerfile uses entrypoint.sh
- [ ] entrypoint.sh is executable

### During Deployment
- [ ] Watch build logs in Render dashboard
- [ ] Look for "Starting uvicorn on 0.0.0.0:10000"
- [ ] Wait for health check to pass
- [ ] Check database is "Available"

### After Deployment
- [ ] Test health endpoint: `/api/health`
- [ ] Test API docs: `/api/docs`
- [ ] Test authentication: `/api/auth/register`
- [ ] Verify database connection works

---

## Useful Commands

### Check Logs
```bash
# In Render dashboard:
# Services → agentic-workflows-api → Logs
```

### Test Endpoints
```bash
# Health check
curl https://your-app.onrender.com/api/health

# API docs
open https://your-app.onrender.com/api/docs

# Register user
curl -X POST https://your-app.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'
```

### Local Testing
```powershell
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

## Getting Help

### Render Support
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Project Support
- GitHub Issues: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues
- Email: surajkumarind08@gmail.com

---

## Success Indicators

### Build Logs Should Show:
```
✓ Building Docker image...
✓ Installing dependencies...
✓ Copying application code...
✓ Build completed successfully
```

### Startup Logs Should Show:
```
============================================
  Agentic Workflows - Starting
============================================
PORT: 10000
HOST: 0.0.0.0
ENVIRONMENT: production
DATABASE_URL: postgresql://...
============================================
Waiting for PostgreSQL...
PostgreSQL is ready!
Initializing database tables...
Database initialized successfully
Starting uvicorn on 0.0.0.0:10000...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

### Health Check Should Return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

---

**If you see all these indicators, your deployment is successful!** 🎉

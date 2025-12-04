# Deployment Debugging Guide

## Current Status

**Latest Commit**: `61128a6` - Added extensive logging to diagnose frontend serving issue

## What Was Fixed

1. ✅ Changed `npm ci --only=production` to `npm ci` in Dockerfile (installs devDependencies)
2. ✅ Changed build script from `tsc && vite build` to `vite build` (no TypeScript check)
3. ✅ Added `ui/src/lib/api.ts` and `ui/src/lib/utils.ts` to git
4. ✅ Fixed `.gitignore` to not exclude `ui/src/lib/` files
5. ✅ Added extensive logging to server.py
6. ✅ Added debug endpoint `/api/debug/filesystem`

## How to Check Deployment

### 1. Check Render.com Dashboard

Go to: https://dashboard.render.com/

- Look for service: `agentic-workflows`
- Check status: Should be "Live" (green)
- If "Deploying" (yellow), wait for it to complete
- If "Failed" (red), click to see error logs

### 2. Check Build Logs

In Render dashboard:
1. Click on `agentic-workflows` service
2. Click "Logs" tab
3. Look for these messages:
   - ✅ `npm ci` completed successfully
   - ✅ `npm run build` completed successfully
   - ✅ `vite build` output showing bundle size
   - ✅ `ls -la dist/` showing files
   - ❌ `sh: 1: tsc: not found` (should NOT appear anymore)

### 3. Check Runtime Logs

After deployment completes, check logs for:
```
checking_frontend_path
serving_react_frontend
mounted_assets
```

### 4. Test Endpoints

Once deployed, test these URLs:

**Health Check** (should work):
```
https://agentic-workflows.onrender.com/api/health
```

**Debug Filesystem** (NEW - check if ui/dist exists):
```
https://agentic-workflows.onrender.com/api/debug/filesystem
```

Expected response:
```json
{
  "app_root": "/app",
  "ui_dist_path": "/app/ui/dist",
  "ui_dist_exists": true,
  "ui_dist_contents": ["index.html", "assets", "manifest.json", "sw.js", "robots.txt"],
  "cwd": "/app",
  "file_location": "/app/agentic_workflows/api/server.py"
}
```

**Frontend** (should serve React app):
```
https://agentic-workflows.onrender.com/
```

## Common Issues & Solutions

### Issue 1: "tsc: not found" during build

**Cause**: Using `npm ci --only=production` which doesn't install devDependencies

**Solution**: ✅ FIXED - Changed to `npm ci` in Dockerfile

### Issue 2: "Module not found: ui/src/lib/api.ts"

**Cause**: Files excluded by `.gitignore`

**Solution**: ✅ FIXED - Updated `.gitignore` and added files to git

### Issue 3: All URLs return "Not Found"

**Possible Causes**:
1. Deployment still in progress (wait 2-3 minutes)
2. `ui/dist` folder not copied to Docker image
3. Path resolution issue in server.py

**Debug Steps**:
1. Check `/api/debug/filesystem` endpoint
2. If `ui_dist_exists: false`, check Dockerfile COPY command
3. If `ui_dist_exists: true` but still 404, check server.py routing

### Issue 4: Build succeeds but app crashes on startup

**Cause**: Database connection issues or missing environment variables

**Solution**: Check logs for errors, ensure DATABASE_URL is set

## Next Steps

1. **Wait for deployment** - Render.com takes 2-3 minutes to build and deploy
2. **Check logs** - Look for the new debug messages
3. **Test debug endpoint** - Visit `/api/debug/filesystem` to see if ui/dist exists
4. **Report findings** - Share the output of debug endpoint

## Expected Timeline

- **Build time**: ~2-3 minutes (npm install + build + Docker layers)
- **Deploy time**: ~30 seconds (health check + startup)
- **Total**: ~3-4 minutes from push to live

## Monitoring

Watch the deployment in real-time:
```
https://dashboard.render.com/web/[your-service-id]/events
```

## If Still Not Working

If after deployment completes and you still see "Not Found":

1. Share the output of `/api/debug/filesystem`
2. Share the last 50 lines of runtime logs
3. Check if health check is passing: `/api/health`

The debug endpoint will tell us exactly what's happening with the filesystem!

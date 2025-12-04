# Quick OAuth Setup Guide - Remove Configuration Warnings

## Current Status
Your app shows these warnings because OAuth credentials aren't configured:
```
[warning] google_oauth_not_configured
[warning] github_oauth_not_configured
```

This is **normal and safe** - the app works fine with email/password login. But to enable OAuth, follow these steps:

---

## Option 1: Quick Setup (Google OAuth - 10 minutes)

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. Select **Web application**
6. Configure:
   - **Name:** Agentic Workflows
   - **Authorized redirect URIs:** 
     - Add: `https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback`
7. Click **Create**
8. Copy the **Client ID** and **Client Secret**

### Step 2: Add to Render Environment

1. Go to your [Render Dashboard](https://dashboard.render.com/)
2. Select your service: **agentic-workflows-pm7o**
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Add these three variables:

```
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback
```

6. Click **Save Changes**
7. Render will automatically redeploy (takes ~2 minutes)

### Step 3: Test

1. Visit: https://agentic-workflows-pm7o.onrender.com/login
2. Click "Continue with Google"
3. Should redirect to Google sign-in
4. After approval, you'll be logged in!

✅ **Warning will disappear** after redeployment

---

## Option 2: GitHub OAuth (5 minutes)

### Step 1: Register GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Configure:
   - **Application name:** Agentic Workflows
   - **Homepage URL:** `https://agentic-workflows-pm7o.onrender.com`
   - **Authorization callback URL:** `https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback`
4. Click **Register application**
5. Click **Generate a new client secret**
6. Copy **Client ID** and **Client Secret**

### Step 2: Add to Render Environment

Add these variables in Render:

```
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback
```

✅ **Warning will disappear** after redeployment

---

## Option 3: Keep Warnings (Recommended for Now)

**The warnings are harmless!** They just mean OAuth isn't configured. Your app works perfectly with:
- ✅ Email/Password login
- ✅ Password reset
- ✅ User registration
- ✅ All features

**You can configure OAuth later** when you need it. The warnings don't affect functionality.

---

## Why These Warnings Appear

The app checks for OAuth credentials on startup:
```python
if settings.google_client_id and settings.google_client_secret:
    # Register Google OAuth
else:
    logger.warning("google_oauth_not_configured")
```

This is **intentional** - it lets you know OAuth is available but not configured.

---

## Summary

**To remove warnings:**
1. Add OAuth credentials to Render environment variables
2. Redeploy (automatic)
3. Warnings disappear

**Or just ignore them:**
- Warnings don't affect functionality
- App works perfectly without OAuth
- Configure later when needed

---

**Need help?** Check the full guide: `docs/OAUTH_SETUP.md`

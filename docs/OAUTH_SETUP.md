# OAuth Setup Guide

## Overview

This guide explains how to set up OAuth authentication with Google and GitHub for your Agentic Workflows application.

---

## Why OAuth is Not Working

OAuth requires API credentials from Google and GitHub. These credentials are **not included** in the repository for security reasons. You need to create your own OAuth applications and configure the credentials.

---

## Google OAuth Setup

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure the OAuth consent screen if prompted:
   - User Type: External
   - App name: Agentic Workflows
   - User support email: Your email
   - Developer contact: Your email
6. Application type: **Web application**
7. Name: Agentic Workflows
8. Authorized redirect URIs:
   ```
   http://localhost:8000/api/auth/google/callback
   https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback
   ```
9. Click **Create**
10. Copy the **Client ID** and **Client Secret**

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
GOOGLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback
```

### Step 3: Configure on Render.com

1. Go to your Render.com dashboard
2. Select your service
3. Go to **Environment** tab
4. Add environment variables:
   - `GOOGLE_CLIENT_ID`: Your Google Client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google Client Secret
   - `GOOGLE_REDIRECT_URI`: Your callback URL

---

## GitHub OAuth Setup

### Step 1: Create GitHub OAuth App

1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click **OAuth Apps** → **New OAuth App**
3. Fill in the details:
   - Application name: Agentic Workflows
   - Homepage URL: `https://agentic-workflows-pm7o.onrender.com`
   - Authorization callback URL: `https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback`
4. Click **Register application**
5. Copy the **Client ID**
6. Click **Generate a new client secret**
7. Copy the **Client Secret** (you won't be able to see it again!)

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
GITHUB_CLIENT_ID=your-github-client-id-here
GITHUB_CLIENT_SECRET=your-github-client-secret-here
GITHUB_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback
```

### Step 3: Configure on Render.com

1. Go to your Render.com dashboard
2. Select your service
3. Go to **Environment** tab
4. Add environment variables:
   - `GITHUB_CLIENT_ID`: Your GitHub Client ID
   - `GITHUB_CLIENT_SECRET`: Your GitHub Client Secret
   - `GITHUB_REDIRECT_URI`: Your callback URL

---

## Apple OAuth Setup (Optional)

### Step 1: Create Apple Sign In

1. Go to [Apple Developer Portal](https://developer.apple.com/)
2. Navigate to **Certificates, Identifiers & Profiles**
3. Create a new **App ID**
4. Enable **Sign in with Apple**
5. Create a **Services ID**
6. Configure the redirect URI:
   ```
   https://agentic-workflows-pm7o.onrender.com/api/auth/apple/callback
   ```
7. Download the private key
8. Note your Team ID, Key ID, and Client ID

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
APPLE_CLIENT_ID=your-apple-client-id-here
APPLE_CLIENT_SECRET=your-apple-client-secret-here
APPLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/apple/callback
```

---

## Testing OAuth Locally

### Step 1: Update Local Redirect URIs

For local testing, add these redirect URIs to your OAuth apps:

**Google:**
```
http://localhost:8000/api/auth/google/callback
```

**GitHub:**
```
http://localhost:8000/api/auth/github/callback
```

### Step 2: Update .env File

```bash
# Local development
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/github/callback
```

### Step 3: Test

1. Start your backend: `uvicorn agentic_workflows.api.server:app --reload`
2. Start your frontend: `cd ui && npm run dev`
3. Navigate to `http://localhost:5173/login`
4. Click on Google or GitHub button
5. Complete the OAuth flow

---

## Troubleshooting

### Error: "OAuth not configured"

**Cause**: OAuth credentials are not set in environment variables.

**Solution**: 
1. Verify credentials are set in `.env` file
2. Restart your application
3. Check Render.com environment variables

### Error: "Redirect URI mismatch"

**Cause**: The redirect URI in your OAuth app doesn't match the one in your application.

**Solution**:
1. Check the redirect URI in Google/GitHub OAuth app settings
2. Ensure it matches exactly (including http/https and trailing slashes)
3. Common URIs:
   - Production: `https://agentic-workflows-pm7o.onrender.com/api/auth/{provider}/callback`
   - Local: `http://localhost:8000/api/auth/{provider}/callback`

### Error: "Invalid client"

**Cause**: Client ID or Client Secret is incorrect.

**Solution**:
1. Verify you copied the credentials correctly
2. Check for extra spaces or newlines
3. Regenerate credentials if needed

### OAuth Button Does Nothing

**Cause**: Frontend is not properly configured or OAuth is not set up.

**Solution**:
1. Check browser console for errors
2. Verify backend is running
3. Check that OAuth credentials are configured
4. The app will show a friendly error message if OAuth is not configured

---

## Security Best Practices

### 1. Never Commit Credentials

✅ **DO**: Use environment variables
❌ **DON'T**: Hardcode credentials in code

### 2. Use Different Credentials for Development and Production

- Development: Use separate OAuth apps with localhost redirect URIs
- Production: Use production OAuth apps with your domain

### 3. Rotate Credentials Regularly

- Regenerate OAuth secrets every 90 days
- Update environment variables immediately

### 4. Restrict Redirect URIs

Only add the redirect URIs you actually use:
- ✅ `https://your-domain.com/api/auth/google/callback`
- ❌ `https://*.com/callback` (too broad)

### 5. Monitor OAuth Usage

- Check Google Cloud Console for unusual activity
- Review GitHub OAuth app access logs
- Set up alerts for failed authentication attempts

---

## Current Status

### ✅ What's Working

- Email/password authentication
- User registration
- Login/logout
- Session management
- JWT tokens

### ⚠️ What Needs Configuration

- Google OAuth (requires credentials)
- GitHub OAuth (requires credentials)
- Apple OAuth (requires credentials)

### 📝 User Experience

When OAuth is not configured:
1. OAuth buttons are visible on login/register pages
2. Clicking them shows a friendly error message
3. Users are informed to use email/password login
4. No application crashes or errors

---

## Quick Setup Checklist

### For Local Development

- [ ] Create Google OAuth app
- [ ] Create GitHub OAuth app
- [ ] Add credentials to `.env` file
- [ ] Add localhost redirect URIs
- [ ] Restart backend server
- [ ] Test OAuth flow

### For Production (Render.com)

- [ ] Create Google OAuth app (production)
- [ ] Create GitHub OAuth app (production)
- [ ] Add production redirect URIs
- [ ] Add credentials to Render environment variables
- [ ] Redeploy application
- [ ] Test OAuth flow on production

---

## Example .env File

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agentic_workflows

# Security
SECRET_KEY=your-secret-key-here-32-characters-minimum

# OAuth - Google
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
GOOGLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback

# OAuth - GitHub
GITHUB_CLIENT_ID=Iv1.abcdefghijklmnop
GITHUB_CLIENT_SECRET=abcdefghijklmnopqrstuvwxyz1234567890abcd
GITHUB_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback

# OAuth - Apple (Optional)
# APPLE_CLIENT_ID=com.yourcompany.agenticworkflows
# APPLE_CLIENT_SECRET=your-apple-client-secret
# APPLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/apple/callback

# Environment
ENVIRONMENT=production
DEBUG=false
```

---

## Support

If you need help setting up OAuth:

1. Check the [GitHub Issues](https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues)
2. Review the [API Documentation](https://agentic-workflows-pm7o.onrender.com/api/docs)
3. Email: surajkumarind08@gmail.com

---

**Last Updated**: December 5, 2025  
**Status**: OAuth setup required for Google/GitHub login  
**Alternative**: Use email/password authentication (fully functional)

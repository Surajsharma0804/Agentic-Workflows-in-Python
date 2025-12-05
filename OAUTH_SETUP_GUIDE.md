# OAuth Setup Guide for Agentic Workflows

This guide will help you enable Google and GitHub OAuth login for your application.

## Prerequisites
- Your app is deployed on Render.com: https://agentic-workflows-pm7o.onrender.com
- You have access to Google Cloud Console and GitHub Developer Settings

---

## 1. Google OAuth Setup

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. Configure OAuth consent screen if prompted:
   - User Type: **External**
   - App name: **Agentic Workflows**
   - User support email: Your email
   - Developer contact: Your email
   - Add scopes: `email`, `profile`, `openid`
   - Add test users (your email)

### Step 2: Create OAuth Client ID

1. Application type: **Web application**
2. Name: **Agentic Workflows Production**
3. Authorized JavaScript origins:
   ```
   https://agentic-workflows-pm7o.onrender.com
   ```
4. Authorized redirect URIs:
   ```
   https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback
   ```
5. Click **Create**
6. **Copy the Client ID and Client Secret** (you'll need these)

### Step 3: Add to Render.com

1. Go to your Render.com dashboard
2. Select your **agentic-workflows** service
3. Go to **Environment** tab
4. Add these environment variables:
   ```
   GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret-here
   GOOGLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback
   ```
5. Click **Save Changes** (this will trigger a redeploy)

---

## 2. GitHub OAuth Setup

### Step 1: Create GitHub OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **OAuth Apps** → **New OAuth App**
3. Fill in the details:
   - Application name: **Agentic Workflows**
   - Homepage URL: `https://agentic-workflows-pm7o.onrender.com`
   - Application description: **AI-Powered Workflow Automation Platform**
   - Authorization callback URL: `https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback`
4. Click **Register application**
5. Click **Generate a new client secret**
6. **Copy the Client ID and Client Secret**

### Step 2: Add to Render.com

1. Go to your Render.com dashboard
2. Select your **agentic-workflows** service
3. Go to **Environment** tab
4. Add these environment variables:
   ```
   GITHUB_CLIENT_ID=your-github-client-id
   GITHUB_CLIENT_SECRET=your-github-client-secret
   GITHUB_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback
   ```
5. Click **Save Changes** (this will trigger a redeploy)

---

## 3. Apple Sign In Setup (Optional)

Apple Sign In requires:
- Apple Developer Account ($99/year)
- More complex setup with certificates

**For now, skip Apple Sign In** and focus on Google + GitHub.

---

## 4. Testing OAuth

After adding the environment variables and redeploying:

1. Wait 5-10 minutes for Render.com to redeploy
2. Go to https://agentic-workflows-pm7o.onrender.com/login
3. Click **Continue with Google** or **Continue with GitHub**
4. You should be redirected to the OAuth provider
5. After authorization, you'll be logged in automatically

---

## 5. Troubleshooting

### "OAuth is not configured" error
- Check that environment variables are set correctly on Render.com
- Verify the redirect URIs match exactly (including https://)
- Wait for the redeploy to complete

### "Redirect URI mismatch" error
- Go back to Google Cloud Console / GitHub OAuth settings
- Verify the redirect URI is exactly: `https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback`
- No trailing slashes, must use https://

### OAuth works but login fails
- Check Render.com logs for errors
- Verify SECRET_KEY is set in environment variables
- Ensure DATABASE_URL is configured correctly

---

## Quick Setup Checklist

### Google OAuth
- [ ] Create Google Cloud project
- [ ] Configure OAuth consent screen
- [ ] Create OAuth client ID
- [ ] Add authorized redirect URI
- [ ] Copy Client ID and Secret
- [ ] Add to Render.com environment variables
- [ ] Wait for redeploy
- [ ] Test login

### GitHub OAuth
- [ ] Create GitHub OAuth App
- [ ] Set callback URL
- [ ] Generate client secret
- [ ] Copy Client ID and Secret
- [ ] Add to Render.com environment variables
- [ ] Wait for redeploy
- [ ] Test login

---

## Environment Variables Summary

Add these to Render.com → Environment tab:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://agentic-workflows-pm7o.onrender.com/api/auth/github/callback
```

---

## Security Notes

1. **Never commit OAuth secrets to Git**
2. Keep Client Secrets secure
3. Only add your domain to authorized origins
4. Use HTTPS only (never HTTP in production)
5. Regularly rotate secrets if compromised

---

## Support

If you encounter issues:
1. Check Render.com logs: Dashboard → Logs tab
2. Verify environment variables are set
3. Test with email/password login first
4. Check OAuth provider dashboards for errors

---

**That's it!** Once configured, users can sign in with Google or GitHub in addition to email/password.

# OAuth2 Authentication Setup Guide

Complete guide to setting up Google, Apple, and GitHub OAuth authentication for Agentic Workflows.

## Overview

OAuth2 provides secure, industry-standard authentication that allows users to sign in with their existing accounts without creating new passwords. This implementation supports:

- ✅ **Google Sign-In** - Most popular OAuth provider
- ✅ **Apple Sign In** - Required for iOS apps
- ✅ **GitHub OAuth** - Popular with developers

## Architecture

### Flow Diagram

```
User clicks "Sign in with Google"
    ↓
Frontend redirects to /api/auth/google/login
    ↓
Backend redirects to Google OAuth consent screen
    ↓
User approves access
    ↓
Google redirects to /api/auth/google/callback
    ↓
Backend exchanges code for access token
    ↓
Backend fetches user info from Google
    ↓
Backend creates/updates user in database
    ↓
Backend generates JWT token
    ↓
Backend redirects to /auth/callback?token=JWT
    ↓
Frontend stores token and redirects to dashboard
```

## Setup Instructions

### 1. Google OAuth Setup

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Google+ API" for your project

#### Step 2: Create OAuth Credentials

1. Navigate to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Web application**
4. Configure:
   - **Name:** Agentic Workflows
   - **Authorized JavaScript origins:**
     - `http://localhost:8000` (development)
     - `https://your-domain.com` (production)
   - **Authorized redirect URIs:**
     - `http://localhost:8000/api/auth/google/callback` (development)
     - `https://your-domain.com/api/auth/google/callback` (production)
5. Click **Create**
6. Copy **Client ID** and **Client Secret**

#### Step 3: Configure Environment Variables

Add to your `.env` file:

```bash
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret-here
GOOGLE_REDIRECT_URI=https://your-domain.com/api/auth/google/callback
```

#### Testing Google OAuth

```bash
# Development
curl http://localhost:8000/api/auth/google/login

# Production
curl https://your-domain.com/api/auth/google/login
```

---

### 2. GitHub OAuth Setup

#### Step 1: Register OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Configure:
   - **Application name:** Agentic Workflows
   - **Homepage URL:** `https://your-domain.com`
   - **Authorization callback URL:** `https://your-domain.com/api/auth/github/callback`
4. Click **Register application**
5. Click **Generate a new client secret**
6. Copy **Client ID** and **Client Secret**

#### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
GITHUB_CLIENT_ID=Iv1.1234567890abcdef
GITHUB_CLIENT_SECRET=1234567890abcdef1234567890abcdef12345678
GITHUB_REDIRECT_URI=https://your-domain.com/api/auth/github/callback
```

#### Testing GitHub OAuth

```bash
# Development
curl http://localhost:8000/api/auth/github/login

# Production
curl https://your-domain.com/api/auth/github/callback
```

---

### 3. Apple Sign In Setup

#### Step 1: Create App ID

1. Go to [Apple Developer Portal](https://developer.apple.com/account/resources/identifiers/list)
2. Click **+** to create new identifier
3. Select **App IDs** → **Continue**
4. Select **App** → **Continue**
5. Configure:
   - **Description:** Agentic Workflows
   - **Bundle ID:** `com.yourcompany.agentic-workflows`
   - **Capabilities:** Enable **Sign In with Apple**
6. Click **Continue** → **Register**

#### Step 2: Create Services ID

1. Click **+** to create new identifier
2. Select **Services IDs** → **Continue**
3. Configure:
   - **Description:** Agentic Workflows Web
   - **Identifier:** `com.yourcompany.agentic-workflows.web`
   - Enable **Sign In with Apple**
4. Click **Configure** next to Sign In with Apple
5. Configure:
   - **Primary App ID:** Select your App ID from Step 1
   - **Domains and Subdomains:** `your-domain.com`
   - **Return URLs:** `https://your-domain.com/api/auth/apple/callback`
6. Click **Save** → **Continue** → **Register**

#### Step 3: Create Private Key

1. Go to **Keys** section
2. Click **+** to create new key
3. Configure:
   - **Key Name:** Agentic Workflows Sign In Key
   - Enable **Sign In with Apple**
   - Click **Configure** → Select your Primary App ID
4. Click **Continue** → **Register**
5. **Download** the `.p8` file (you can only download once!)
6. Note the **Key ID** (10 characters)

#### Step 4: Get Team ID

1. Go to **Membership** section
2. Copy your **Team ID** (10 characters)

#### Step 5: Configure Environment Variables

Add to your `.env` file:

```bash
APPLE_CLIENT_ID=com.yourcompany.agentic-workflows.web
APPLE_TEAM_ID=ABC1234DEF
APPLE_KEY_ID=XYZ9876WVU
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg...\n-----END PRIVATE KEY-----
APPLE_REDIRECT_URI=https://your-domain.com/api/auth/apple/callback
```

**Note:** For the private key, replace newlines with `\n` in the environment variable.

#### Testing Apple Sign In

Apple Sign In requires HTTPS and a registered domain, so testing locally is limited. Use production environment for testing.

---

## Render.com Deployment

### Step 1: Add Environment Variables

In your Render dashboard:

1. Go to your service
2. Navigate to **Environment** tab
3. Add all OAuth variables:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-app.onrender.com/api/auth/google/callback

GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://your-app.onrender.com/api/auth/github/callback

APPLE_CLIENT_ID=com.yourcompany.agentic-workflows.web
APPLE_TEAM_ID=your-team-id
APPLE_KEY_ID=your-key-id
APPLE_PRIVATE_KEY=your-private-key-with-newlines-escaped
APPLE_REDIRECT_URI=https://your-app.onrender.com/api/auth/apple/callback
```

### Step 2: Update OAuth Provider Settings

Update redirect URIs in each provider's console:

**Google:**
- Add `https://your-app.onrender.com/api/auth/google/callback`

**GitHub:**
- Update Authorization callback URL to `https://your-app.onrender.com/api/auth/github/callback`

**Apple:**
- Update Return URL to `https://your-app.onrender.com/api/auth/apple/callback`

### Step 3: Deploy

```bash
git add -A
git commit -m "feat: add OAuth2 authentication"
git push origin main
```

Render will automatically deploy with the new OAuth configuration.

---

## Security Best Practices

### 1. Environment Variables

✅ **DO:**
- Store credentials in environment variables
- Use different credentials for dev/staging/production
- Rotate secrets regularly
- Use secret management services (AWS Secrets Manager, etc.)

❌ **DON'T:**
- Commit credentials to git
- Share credentials in plain text
- Use production credentials in development
- Hardcode credentials in code

### 2. Redirect URIs

✅ **DO:**
- Use HTTPS in production
- Whitelist specific redirect URIs
- Validate redirect URIs on backend
- Use exact matches (not wildcards)

❌ **DON'T:**
- Allow arbitrary redirect URIs
- Use HTTP in production
- Use wildcards in redirect URIs
- Trust client-provided redirect URIs

### 3. Token Handling

✅ **DO:**
- Store tokens securely (httpOnly cookies or secure storage)
- Implement token expiration
- Validate tokens on every request
- Use HTTPS for all token transmission

❌ **DON'T:**
- Store tokens in localStorage (XSS vulnerable)
- Use long-lived tokens without refresh
- Transmit tokens over HTTP
- Log tokens in application logs

### 4. User Data

✅ **DO:**
- Request minimum required scopes
- Respect user privacy
- Implement data retention policies
- Allow users to disconnect OAuth accounts

❌ **DON'T:**
- Request unnecessary permissions
- Store sensitive OAuth tokens
- Share user data with third parties
- Keep data indefinitely

---

## Troubleshooting

### Google OAuth Issues

**Error: redirect_uri_mismatch**
- Solution: Ensure redirect URI in Google Console exactly matches your configured URI
- Check for trailing slashes, http vs https, port numbers

**Error: invalid_client**
- Solution: Verify Client ID and Client Secret are correct
- Check environment variables are loaded

**Error: access_denied**
- Solution: User declined authorization
- This is normal user behavior, handle gracefully

### GitHub OAuth Issues

**Error: redirect_uri_mismatch**
- Solution: Update Authorization callback URL in GitHub OAuth App settings

**Error: bad_verification_code**
- Solution: Code expired or already used
- Ensure user completes flow quickly
- Don't reuse authorization codes

**No email returned**
- Solution: User's email is private
- Request `user:email` scope
- Fetch emails from `/user/emails` endpoint

### Apple Sign In Issues

**Error: invalid_client**
- Solution: Verify Services ID matches APPLE_CLIENT_ID
- Check Team ID and Key ID are correct

**Error: invalid_grant**
- Solution: Private key format is incorrect
- Ensure newlines are properly escaped in environment variable
- Verify key hasn't expired (valid for 6 months)

**Token verification fails**
- Solution: Check audience matches your Services ID
- Verify issuer is `https://appleid.apple.com`
- Ensure using correct public keys from Apple

### General Issues

**OAuth not working locally**
- Solution: Some providers require HTTPS
- Use ngrok or similar for local HTTPS testing
- Or test directly on staging/production

**Database errors**
- Solution: Run migrations: `alembic upgrade head`
- Check database connection
- Verify OAuth fields exist in users table

**Token not being set**
- Solution: Check browser console for errors
- Verify `/auth/callback` route exists
- Check token is in URL parameters

---

## Testing

### Manual Testing

1. **Google:**
   ```
   Visit: http://localhost:8000/api/auth/google/login
   Expected: Redirect to Google consent screen
   After approval: Redirect to dashboard with user logged in
   ```

2. **GitHub:**
   ```
   Visit: http://localhost:8000/api/auth/github/login
   Expected: Redirect to GitHub authorization page
   After approval: Redirect to dashboard with user logged in
   ```

3. **Apple:**
   ```
   Visit: https://your-domain.com/api/auth/apple/login
   Expected: Redirect to Apple Sign In page
   After approval: Redirect to dashboard with user logged in
   ```

### Automated Testing

```python
# Test OAuth endpoints exist
def test_oauth_endpoints():
    response = requests.get("http://localhost:8000/api/auth/google/login")
    assert response.status_code in [302, 501]  # Redirect or not configured
    
    response = requests.get("http://localhost:8000/api/auth/github/login")
    assert response.status_code in [302, 501]
```

---

## Monitoring

### Metrics to Track

- OAuth login attempts
- OAuth login successes
- OAuth login failures
- Provider-specific error rates
- Average OAuth flow completion time

### Logging

```python
logger.info("oauth_login_initiated", provider="google", user_email="user@example.com")
logger.info("oauth_login_success", provider="google", user_id=123)
logger.error("oauth_login_failed", provider="google", error="invalid_grant")
```

### Alerts

Set up alerts for:
- High OAuth failure rate (>10%)
- Provider API errors
- Token verification failures
- Unusual OAuth activity patterns

---

## FAQ

**Q: Can users sign in with multiple providers?**
A: Yes, if they use the same email address, accounts will be linked automatically.

**Q: What happens if a user's email changes?**
A: OAuth providers typically don't allow email changes. If needed, user should create new account.

**Q: Can I disable password login and use only OAuth?**
A: Yes, but keep password reset for account recovery. Some users prefer passwords.

**Q: How do I handle users without email addresses?**
A: All three providers require email. If email is private, request email scope explicitly.

**Q: What if OAuth provider is down?**
A: Always provide alternative login methods (email/password). Show clear error messages.

**Q: How do I test OAuth locally?**
A: Use ngrok for HTTPS tunnel, or test on staging environment. Some providers allow localhost.

---

## Resources

### Official Documentation

- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Apps](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [Apple Sign In](https://developer.apple.com/sign-in-with-apple/)

### Libraries Used

- [Authlib](https://docs.authlib.org/) - OAuth client library
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT token handling
- [httpx](https://www.python-httpx.org/) - Async HTTP client

### Support

- GitHub Issues: [Report OAuth issues](https://github.com/your-repo/issues)
- Email: support@agentic-workflows.com
- Documentation: https://docs.agentic-workflows.com

---

**Last Updated:** December 4, 2024
**Version:** 1.0.0

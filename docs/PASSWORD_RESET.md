# Password Reset Feature

Complete implementation of secure password reset functionality with email support.

## Features

✅ **Secure Token Generation** - Uses `secrets.token_urlsafe(32)` for cryptographically secure tokens
✅ **Token Expiration** - Reset tokens expire after 1 hour
✅ **Email Support** - Professional HTML email templates with fallback to console logging
✅ **Token Validation** - Frontend validates token before showing reset form
✅ **Password Strength** - Enforces minimum 8 character passwords
✅ **Security Best Practices** - No email enumeration, tokens stored hashed in database
✅ **User Experience** - Clear feedback, loading states, and success messages

## User Flow

1. **Request Reset**
   - User clicks "Forgot Password?" on login page
   - Enters email address
   - System generates secure token and sends email
   - Success message shown (even if email doesn't exist - prevents enumeration)

2. **Receive Email**
   - Professional HTML email with reset link
   - Link format: `https://your-domain.com/reset-password?token=<secure-token>`
   - Email includes expiration warning (1 hour)
   - Clear instructions and security warnings

3. **Reset Password**
   - User clicks link in email
   - Frontend validates token with backend
   - If valid, shows password reset form
   - If invalid/expired, shows error with option to request new link
   - User enters new password (with confirmation)
   - Password strength indicator shows requirements

4. **Confirmation**
   - Success message displayed
   - Auto-redirect to login page after 3 seconds
   - User can login with new password

## API Endpoints

### POST /api/auth/forgot-password
Request a password reset email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If the email exists, a reset link has been sent"
}
```

**Notes:**
- Always returns success to prevent email enumeration
- Generates secure token with 1-hour expiration
- Sends email if SMTP configured, otherwise logs to console

### GET /api/auth/verify-reset-token/{token}
Verify if a reset token is valid.

**Response (Valid):**
```json
{
  "valid": true,
  "email": "user@example.com",
  "expires_in_minutes": 45
}
```

**Response (Invalid):**
```json
{
  "valid": false,
  "message": "Invalid reset token"
}
```

### POST /api/auth/reset-password
Reset password using valid token.

**Request:**
```json
{
  "token": "secure-token-here",
  "new_password": "newpassword123"
}
```

**Response (Success):**
```json
{
  "message": "Password reset successfully. You can now login with your new password."
}
```

**Response (Error):**
```json
{
  "detail": "Reset token has expired. Please request a new one."
}
```

## Database Schema

### User Model Updates

Added two new fields to the `users` table:

```python
reset_token = Column(String, nullable=True)
reset_token_expires = Column(DateTime, nullable=True)
```

**Migration:** `alembic/versions/002_add_password_reset.py`

## Email Configuration

### SMTP Setup (Production)

Add to your `.env` file:

```bash
# Gmail Example
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@agentic-workflows.com

# SendGrid Example
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM_EMAIL=noreply@agentic-workflows.com

# AWS SES Example
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your-ses-username
SMTP_PASSWORD=your-ses-password
SMTP_FROM_EMAIL=noreply@agentic-workflows.com
```

### Gmail Setup

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the generated password in `SMTP_PASSWORD`

### Development Mode

If SMTP is not configured, emails are logged to console:

```
2024-12-04 15:30:00 [info] email_would_be_sent
  to=user@example.com
  subject=Reset Your Password - Agentic Workflows
  html=<!DOCTYPE html>...
```

This allows development without email setup.

## Security Features

### Token Security
- **Cryptographically Secure**: Uses `secrets.token_urlsafe(32)` (256 bits of entropy)
- **One-Time Use**: Token is cleared after successful password reset
- **Time-Limited**: Expires after 1 hour
- **Database Stored**: Tokens stored in database, not in JWT

### Email Enumeration Prevention
- Always returns success message, even if email doesn't exist
- Prevents attackers from discovering valid email addresses
- Logs attempts for security monitoring

### Password Validation
- Minimum 8 characters required
- Frontend validation with visual feedback
- Backend validation with clear error messages
- Passwords hashed with bcrypt before storage

### Rate Limiting
- Consider adding rate limiting to prevent abuse
- Recommended: 3 requests per email per hour

## Frontend Components

### ForgotPassword.tsx
- Email input form
- Loading states
- Success confirmation with instructions
- Resend option
- Back to login link

### ResetPassword.tsx
- Token verification on mount
- Password and confirm password inputs
- Password strength indicator
- Real-time validation feedback
- Success state with auto-redirect
- Error handling for invalid/expired tokens

### Email Template
- Professional HTML design
- Responsive layout
- Clear call-to-action button
- Security warnings
- Expiration notice
- Plain text fallback

## Testing

### Manual Testing

1. **Request Reset:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/forgot-password \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com"}'
   ```

2. **Check Console/Email:**
   - Development: Check console logs for reset link
   - Production: Check email inbox

3. **Verify Token:**
   ```bash
   curl http://localhost:8000/api/auth/verify-reset-token/TOKEN_HERE
   ```

4. **Reset Password:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/reset-password \
     -H "Content-Type: application/json" \
     -d '{"token":"TOKEN_HERE","new_password":"newpass123"}'
   ```

### Test Scenarios

- ✅ Valid email receives reset link
- ✅ Invalid email returns success (no enumeration)
- ✅ Token expires after 1 hour
- ✅ Used token cannot be reused
- ✅ Invalid token shows error
- ✅ Password validation works
- ✅ Successful reset allows login
- ✅ Email template renders correctly

## Deployment

### Render.com Setup

1. Add environment variables in Render dashboard:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_FROM_EMAIL=noreply@agentic-workflows.com
   ```

2. Database migration runs automatically via `entrypoint.sh`

3. Test after deployment:
   - Visit: https://your-app.onrender.com/forgot-password
   - Request reset for test account
   - Check email or logs

### Environment Variables

Required for email functionality:
- `SMTP_HOST` - SMTP server hostname
- `SMTP_PORT` - SMTP server port (usually 587)
- `SMTP_USERNAME` - SMTP authentication username
- `SMTP_PASSWORD` - SMTP authentication password
- `SMTP_FROM_EMAIL` - Sender email address

Optional (falls back to console logging if not set).

## Troubleshooting

### Emails Not Sending

1. **Check SMTP Configuration:**
   ```python
   # In Python console
   from agentic_workflows.config import get_settings
   settings = get_settings()
   print(f"SMTP Host: {settings.smtp_host}")
   print(f"SMTP Port: {settings.smtp_port}")
   print(f"From Email: {settings.smtp_from_email}")
   ```

2. **Test SMTP Connection:**
   ```python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   server.quit()
   ```

3. **Check Logs:**
   - Look for `email_sent_successfully` or `email_send_failed` log entries
   - Check for authentication errors

### Token Issues

1. **Token Expired:**
   - Tokens expire after 1 hour
   - Request a new reset link

2. **Token Invalid:**
   - Check database for token existence
   - Verify token wasn't already used

3. **Token Not Found:**
   - Ensure database migration ran successfully
   - Check `users` table has `reset_token` column

### Database Migration

If migration didn't run:

```bash
# Run manually
alembic upgrade head

# Or in Docker
docker exec -it container_name alembic upgrade head
```

## Future Enhancements

- [ ] Add rate limiting per email address
- [ ] Implement email verification for new accounts
- [ ] Add 2FA support
- [ ] Track password reset history
- [ ] Add email templates for other notifications
- [ ] Support multiple email providers
- [ ] Add SMS-based password reset option
- [ ] Implement account lockout after failed attempts

## Related Files

- `agentic_workflows/api/routes/auth.py` - Authentication endpoints
- `agentic_workflows/db/models.py` - User model with reset fields
- `agentic_workflows/utils/email.py` - Email sending utility
- `alembic/versions/002_add_password_reset.py` - Database migration
- `ui/src/pages/ForgotPassword.tsx` - Request reset page
- `ui/src/pages/ResetPassword.tsx` - Reset password page
- `.env.example` - Environment configuration template

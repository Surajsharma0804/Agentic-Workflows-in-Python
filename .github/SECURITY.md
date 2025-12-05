# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to security@example.com or create a private security advisory on GitHub.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to Include

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (Critical: 7 days, High: 14 days, Medium: 30 days)

## Security Best Practices

When deploying this application:

1. **Always set a strong SECRET_KEY** in production
2. **Use HTTPS** for all connections
3. **Keep dependencies updated** regularly
4. **Enable rate limiting** on API endpoints
5. **Use environment variables** for all secrets
6. **Regular security audits** recommended
7. **Monitor logs** for suspicious activity
8. **Backup database** regularly

## Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (React escaping)
- ✅ CSRF protection (token-based)
- ✅ Rate limiting ready
- ✅ Input validation on all endpoints

# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Disclose Publicly

Please do not create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send details to: **surajkumarind08@gmail.com**

Or use GitHub's private vulnerability reporting:
https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/security/advisories/new

### 3. Include Details

Please provide:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Affected versions
- Suggested fix (if any)
- Your contact information

### 4. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest version
2. **Strong Secrets**: Use strong, unique SECRET_KEY and JWT_SECRET_KEY
3. **Environment Variables**: Never commit secrets to git
4. **HTTPS Only**: Always use HTTPS in production
5. **Regular Backups**: Backup your database regularly
6. **Monitor Logs**: Check logs for suspicious activity
7. **Rate Limiting**: Enable rate limiting in production
8. **OAuth Credentials**: Keep OAuth credentials secure

### For Developers

1. **Input Validation**: Validate all user inputs
2. **SQL Injection**: Use parameterized queries (SQLAlchemy ORM)
3. **XSS Prevention**: Sanitize outputs
4. **CSRF Protection**: Use CSRF tokens
5. **Authentication**: Require authentication on sensitive endpoints
6. **Authorization**: Check user permissions
7. **Secrets Management**: Use environment variables
8. **Dependencies**: Keep dependencies updated
9. **Code Review**: Review all code changes
10. **Security Testing**: Test for common vulnerabilities

## Known Security Features

### Implemented

- ✅ JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ HTTPS enforcement (production)
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Input validation (Pydantic)
- ✅ Rate limiting (configurable)
- ✅ Session management
- ✅ OAuth2 support
- ✅ Audit logging
- ✅ Error handling
- ✅ Non-root Docker user

### Recommended Additional Measures

- Enable rate limiting in production
- Configure OAuth providers securely
- Use strong SECRET_KEY (32+ characters)
- Enable database backups
- Monitor application logs
- Set up error tracking (Sentry)
- Regular security audits
- Dependency scanning

## Security Configuration

### Required Environment Variables

```bash
# Strong secret keys (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=<strong-random-key-32-chars-min>
JWT_SECRET_KEY=<strong-random-key-32-chars-min>

# Production settings
ENVIRONMENT=production
DEBUG=false

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@host:port/database

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### OAuth Security

When configuring OAuth:
1. Use HTTPS redirect URIs only
2. Keep client secrets secure
3. Validate redirect URIs
4. Use state parameter for CSRF protection
5. Limit OAuth scopes to minimum required

## Vulnerability Disclosure

Once a vulnerability is fixed:
1. We will release a security patch
2. Update CHANGELOG.md
3. Notify affected users
4. Credit the reporter (if desired)
5. Publish security advisory

## Security Updates

Subscribe to security updates:
- Watch this repository on GitHub
- Enable GitHub security alerts
- Follow release notes

## Contact

- **Security Email**: surajkumarind08@gmail.com
- **GitHub Security**: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/security
- **General Issues**: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python/issues

## Acknowledgments

We appreciate security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged in our security advisories (unless they prefer to remain anonymous).

---

**Last Updated**: December 2025

"""OAuth2 authentication utilities for Google, Apple, and GitHub."""
from typing import Optional, Dict, Any
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import structlog
import httpx

from ..config import get_settings

logger = structlog.get_logger()
settings = get_settings()

# Initialize OAuth
config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.google_client_id or "",
    "GOOGLE_CLIENT_SECRET": settings.google_client_secret or "",
    "GITHUB_CLIENT_ID": settings.github_client_id or "",
    "GITHUB_CLIENT_SECRET": settings.github_client_secret or "",
})

oauth = OAuth(config)

# Register Google OAuth
if settings.google_client_id and settings.google_client_secret:
    oauth.register(
        name='google',
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    logger.info("google_oauth_registered")
else:
    logger.warning("google_oauth_not_configured")

# Register GitHub OAuth
if settings.github_client_id and settings.github_client_secret:
    oauth.register(
        name='github',
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
    logger.info("github_oauth_registered")
else:
    logger.warning("github_oauth_not_configured")


async def get_google_user_info(token: str) -> Optional[Dict[str, Any]]:
    """
    Get user information from Google using access token.
    
    Args:
        token: Google OAuth access token
    
    Returns:
        Dict with user info or None if failed
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            user_info = response.json()
            
            return {
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'avatar': user_info.get('picture'),
                'provider': 'google',
                'provider_id': user_info.get('id'),
                'is_verified': user_info.get('verified_email', False)
            }
    except Exception as e:
        logger.error("google_user_info_failed", error=str(e))
        return None


async def get_github_user_info(token: str) -> Optional[Dict[str, Any]]:
    """
    Get user information from GitHub using access token.
    
    Args:
        token: GitHub OAuth access token
    
    Returns:
        Dict with user info or None if failed
    """
    try:
        async with httpx.AsyncClient() as client:
            # Get user profile
            response = await client.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'Bearer {token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            response.raise_for_status()
            user_info = response.json()
            
            # Get primary email
            email_response = await client.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f'Bearer {token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            email_response.raise_for_status()
            emails = email_response.json()
            
            # Find primary verified email
            primary_email = next(
                (e['email'] for e in emails if e['primary'] and e['verified']),
                user_info.get('email')
            )
            
            return {
                'email': primary_email,
                'name': user_info.get('name') or user_info.get('login'),
                'avatar': user_info.get('avatar_url'),
                'provider': 'github',
                'provider_id': str(user_info.get('id')),
                'is_verified': True  # GitHub emails are verified
            }
    except Exception as e:
        logger.error("github_user_info_failed", error=str(e))
        return None


async def verify_apple_token(id_token: str) -> Optional[Dict[str, Any]]:
    """
    Verify Apple Sign In token and extract user information.
    
    Args:
        id_token: Apple ID token (JWT)
    
    Returns:
        Dict with user info or None if failed
    """
    try:
        import jwt
        from jwt import PyJWKClient
        
        # Get Apple's public keys
        jwks_client = PyJWKClient('https://appleid.apple.com/auth/keys')
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        
        # Verify and decode token
        payload = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=settings.apple_client_id,
            issuer='https://appleid.apple.com'
        )
        
        return {
            'email': payload.get('email'),
            'name': payload.get('name', 'Apple User'),  # Apple doesn't always provide name
            'avatar': None,  # Apple doesn't provide avatar
            'provider': 'apple',
            'provider_id': payload.get('sub'),
            'is_verified': payload.get('email_verified', False)
        }
    except Exception as e:
        logger.error("apple_token_verification_failed", error=str(e))
        return None

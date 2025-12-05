"""Authentication endpoints with real database integration."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
import jwt
import secrets
import structlog

from ...db.database import get_db
from ...db.models import User
from ...config import get_settings
from ...utils.email import send_password_reset_email
from ...utils.oauth import oauth, get_google_user_info, get_github_user_info, verify_apple_token

logger = structlog.get_logger()
router = APIRouter()
settings = get_settings()

# JWT settings - MUST be set via environment variable in production
SECRET_KEY = settings.secret_key
if SECRET_KEY == "change-me-in-production":
    import warnings
    warnings.warn(
        "WARNING: Using default SECRET_KEY! Set SECRET_KEY environment variable in production!",
        RuntimeWarning
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    company: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user with database storage."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered. Please use a different email or login."
        )
    
    # Validate password strength
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Create new user
    hashed_password = User.hash_password(request.password)
    new_user = User(
        email=request.email,
        name=request.name,
        company=request.company,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True,  # Auto-verify for now
        role="user"
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": new_user.email, "user_id": new_user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user.to_dict()
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user with email and password validation."""
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials."
        )
    
    # Verify password
    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials."
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled. Please contact support."
        )
    
    # Create access token
    expires_delta = timedelta(days=7) if request.remember_me else timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=expires_delta
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user.to_dict()
    }


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """Send password reset email with secure token."""
    # Always return success to prevent email enumeration
    response_message = "If the email exists, a reset link has been sent"
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        logger.info("password_reset_requested_nonexistent_email", email=request.email)
        return {"message": response_message}
    
    # Generate secure reset token
    reset_token = secrets.token_urlsafe(32)
    reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    
    # Save token to database
    user.reset_token = reset_token
    user.reset_token_expires = reset_token_expires
    
    try:
        db.commit()
        
        # Get base URL from request
        base_url = str(req.base_url).rstrip('/')
        
        # Send password reset email
        email_sent = send_password_reset_email(
            email=user.email,
            reset_token=reset_token,
            base_url=base_url
        )
        
        if email_sent:
            logger.info("password_reset_email_sent", email=user.email)
        else:
            logger.warning("password_reset_email_failed", email=user.email)
        
    except Exception as e:
        db.rollback()
        logger.error("password_reset_failed", error=str(e), email=request.email)
    
    return {"message": response_message}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password using valid token."""
    # Find user with matching token
    user = db.query(User).filter(User.reset_token == request.token).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token is expired
    if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        # Clear expired token
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new one."
        )
    
    # Validate new password
    if len(request.new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Update password and clear reset token
    user.hashed_password = User.hash_password(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    
    try:
        db.commit()
        logger.info("password_reset_successful", email=user.email)
        
        return {
            "message": "Password reset successfully. You can now login with your new password."
        }
        
    except Exception as e:
        db.rollback()
        logger.error("password_update_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password. Please try again."
        )


@router.get("/verify-reset-token/{token}")
async def verify_reset_token(token: str, db: Session = Depends(get_db)):
    """Verify if a reset token is valid and not expired."""
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return {"valid": False, "message": "Invalid reset token"}
    
    if not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        return {"valid": False, "message": "Reset token has expired"}
    
    return {
        "valid": True,
        "email": user.email,
        "expires_in_minutes": int((user.reset_token_expires - datetime.utcnow()).total_seconds() / 60)
    }


@router.get("/me")
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user from token."""
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.to_dict()


@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)."""
    return {"message": "Successfully logged out"}


# ============================================
# OAuth2 Authentication Endpoints
# ============================================

@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login flow."""
    if not settings.google_client_id or not settings.google_client_secret:
        # Redirect to login with error message
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/login?error=oauth_not_configured&provider=google"
        )
    
    redirect_uri = settings.google_redirect_uri or f"{request.base_url}api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback."""
    try:
        # Get access token
        logger.info("google_callback_started")
        token = await oauth.google.authorize_access_token(request)
        logger.info("google_token_received", has_access_token=bool(token.get('access_token')))
        
        # Get user info
        user_info = await get_google_user_info(token['access_token'])
        logger.info("google_user_info_received", user_info=user_info)
        
        if not user_info:
            logger.error("google_user_info_empty")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from Google"
            )
        
        # Find or create user
        user = db.query(User).filter(
            User.oauth_provider == 'google',
            User.oauth_provider_id == user_info['provider_id']
        ).first()
        
        if not user:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == user_info['email']).first()
            if existing_user:
                # Link OAuth to existing account
                existing_user.oauth_provider = 'google'
                existing_user.oauth_provider_id = user_info['provider_id']
                existing_user.avatar = user_info.get('avatar')
                existing_user.is_verified = user_info.get('is_verified', False)
                user = existing_user
            else:
                # Create new user
                user = User(
                    email=user_info['email'],
                    name=user_info['name'],
                    avatar=user_info.get('avatar'),
                    hashed_password=User.hash_password(secrets.token_urlsafe(32)),  # Random password
                    oauth_provider='google',
                    oauth_provider_id=user_info['provider_id'],
                    is_active=True,
                    is_verified=user_info.get('is_verified', False),
                    role='user'
                )
                db.add(user)
        
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        logger.info("google_oauth_success", email=user.email)
        
        # Redirect to frontend with token
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?token={access_token}&provider=google"
        )
        
    except Exception as e:
        logger.error("google_oauth_failed", error=str(e), error_type=type(e).__name__)
        import traceback
        logger.error("google_oauth_traceback", traceback=traceback.format_exc())
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/login?error=google_auth_failed"
        )


@router.get("/github/login")
async def github_login(request: Request):
    """Initiate GitHub OAuth login flow."""
    if not settings.github_client_id or not settings.github_client_secret:
        # Redirect to login with error message
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/login?error=oauth_not_configured&provider=github"
        )
    
    redirect_uri = settings.github_redirect_uri or f"{request.base_url}api/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    """Handle GitHub OAuth callback."""
    try:
        # Get access token
        token = await oauth.github.authorize_access_token(request)
        
        # Get user info
        user_info = await get_github_user_info(token['access_token'])
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from GitHub"
            )
        
        # Find or create user
        user = db.query(User).filter(
            User.oauth_provider == 'github',
            User.oauth_provider_id == user_info['provider_id']
        ).first()
        
        if not user:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == user_info['email']).first()
            if existing_user:
                # Link OAuth to existing account
                existing_user.oauth_provider = 'github'
                existing_user.oauth_provider_id = user_info['provider_id']
                existing_user.avatar = user_info.get('avatar')
                existing_user.is_verified = user_info.get('is_verified', False)
                user = existing_user
            else:
                # Create new user
                user = User(
                    email=user_info['email'],
                    name=user_info['name'],
                    avatar=user_info.get('avatar'),
                    hashed_password=User.hash_password(secrets.token_urlsafe(32)),  # Random password
                    oauth_provider='github',
                    oauth_provider_id=user_info['provider_id'],
                    is_active=True,
                    is_verified=user_info.get('is_verified', False),
                    role='user'
                )
                db.add(user)
        
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id}
        )
        
        logger.info("github_oauth_success", email=user.email)
        
        # Redirect to frontend with token
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?token={access_token}&provider=github"
        )
        
    except Exception as e:
        logger.error("github_oauth_failed", error=str(e))
        frontend_url = str(request.base_url).rstrip('/')
        return RedirectResponse(
            url=f"{frontend_url}/login?error=github_auth_failed"
        )


@router.post("/apple/callback")
async def apple_callback(
    request: Request,
    id_token: str,
    user: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Handle Apple Sign In callback."""
    try:
        # Verify Apple ID token
        user_info = await verify_apple_token(id_token)
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to verify Apple ID token"
            )
        
        # Apple sends user info only on first sign in
        if user:
            import json
            user_data = json.loads(user)
            user_info['name'] = f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}".strip()
        
        # Find or create user
        db_user = db.query(User).filter(
            User.oauth_provider == 'apple',
            User.oauth_provider_id == user_info['provider_id']
        ).first()
        
        if not db_user:
            # Check if email already exists
            existing_user = db.query(User).filter(User.email == user_info['email']).first()
            if existing_user:
                # Link OAuth to existing account
                existing_user.oauth_provider = 'apple'
                existing_user.oauth_provider_id = user_info['provider_id']
                existing_user.is_verified = user_info.get('is_verified', False)
                db_user = existing_user
            else:
                # Create new user
                db_user = User(
                    email=user_info['email'],
                    name=user_info.get('name', 'Apple User'),
                    hashed_password=User.hash_password(secrets.token_urlsafe(32)),  # Random password
                    oauth_provider='apple',
                    oauth_provider_id=user_info['provider_id'],
                    is_active=True,
                    is_verified=user_info.get('is_verified', False),
                    role='user'
                )
                db.add(db_user)
        
        db.commit()
        db.refresh(db_user)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": db_user.email, "user_id": db_user.id}
        )
        
        logger.info("apple_oauth_success", email=db_user.email)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": db_user.to_dict()
        }
        
    except Exception as e:
        logger.error("apple_oauth_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apple Sign In failed"
        )



# Helper function for protected routes
async def get_current_user_from_token(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Get current user from Authorization header token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

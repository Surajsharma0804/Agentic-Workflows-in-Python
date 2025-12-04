"""Authentication endpoints with real database integration."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
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
async def get_current_user(token: str, db: Session = Depends(get_db)):
    """Get current user from token."""
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

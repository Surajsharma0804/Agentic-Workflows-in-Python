"""Email utility for sending notifications."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import structlog

from ..config import get_settings

logger = structlog.get_logger()
settings = get_settings()


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> bool:
    """
    Send email using SMTP configuration.
    Falls back to console logging if SMTP is not configured.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text email body (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Check if SMTP is configured
    if not settings.smtp_host or not settings.smtp_from_email:
        logger.warning(
            "smtp_not_configured",
            message="SMTP not configured, logging email to console instead"
        )
        logger.info(
            "email_would_be_sent",
            to=to_email,
            subject=subject,
            html=html_content[:200] + "..." if len(html_content) > 200 else html_content
        )
        return True
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.smtp_from_email
        msg['To'] = to_email
        
        # Add text and HTML parts
        if text_content:
            part1 = MIMEText(text_content, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html_content, 'html')
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            if settings.smtp_username and settings.smtp_password:
                server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        
        logger.info("email_sent_successfully", to=to_email, subject=subject)
        return True
        
    except Exception as e:
        logger.error("email_send_failed", error=str(e), to=to_email, subject=subject)
        return False


def send_password_reset_email(email: str, reset_token: str, base_url: str) -> bool:
    """
    Send password reset email with reset link.
    
    Args:
        email: User's email address
        reset_token: Password reset token
        base_url: Base URL of the application
    
    Returns:
        bool: True if email sent successfully
    """
    reset_link = f"{base_url}/reset-password?token={reset_token}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
                padding: 40px;
                color: white;
            }}
            .content {{
                background: white;
                border-radius: 8px;
                padding: 30px;
                margin-top: 20px;
                color: #333;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: rgba(255, 255, 255, 0.8);
            }}
            .warning {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 12px;
                margin: 20px 0;
                border-radius: 4px;
                color: #856404;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Password Reset Request</h1>
            <div class="content">
                <p>Hello,</p>
                <p>We received a request to reset your password for your Agentic Workflows account.</p>
                <p>Click the button below to reset your password:</p>
                <a href="{reset_link}" class="button">Reset Password</a>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #667eea;">{reset_link}</p>
                <div class="warning">
                    <strong>⚠️ Important:</strong>
                    <ul style="margin: 10px 0;">
                        <li>This link will expire in 1 hour</li>
                        <li>If you didn't request this reset, please ignore this email</li>
                        <li>Your password won't change until you create a new one</li>
                    </ul>
                </div>
                <p>If you have any questions, please contact our support team.</p>
                <p>Best regards,<br><strong>Agentic Workflows Team</strong></p>
            </div>
            <div class="footer">
                <p>This is an automated email. Please do not reply to this message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Password Reset Request
    
    Hello,
    
    We received a request to reset your password for your Agentic Workflows account.
    
    Click the link below to reset your password:
    {reset_link}
    
    Important:
    - This link will expire in 1 hour
    - If you didn't request this reset, please ignore this email
    - Your password won't change until you create a new one
    
    If you have any questions, please contact our support team.
    
    Best regards,
    Agentic Workflows Team
    """
    
    return send_email(
        to_email=email,
        subject="Reset Your Password - Agentic Workflows",
        html_content=html_content,
        text_content=text_content
    )

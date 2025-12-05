"""Sentry integration for error tracking and monitoring."""
import os
from typing import Optional
import structlog

logger = structlog.get_logger()


def init_sentry(dsn: Optional[str] = None, environment: str = "production") -> bool:
    """
    Initialize Sentry for error tracking.
    
    Args:
        dsn: Sentry DSN (Data Source Name). If not provided, reads from SENTRY_DSN env var.
        environment: Environment name (production, staging, development)
    
    Returns:
        bool: True if Sentry was initialized successfully, False otherwise
    """
    dsn = dsn or os.getenv("SENTRY_DSN")
    
    if not dsn:
        logger.info("sentry_not_configured", note="Set SENTRY_DSN environment variable to enable error tracking")
        return False
    
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
        from sentry_sdk.integrations.redis import RedisIntegration
        
        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            traces_sample_rate=0.1 if environment == "production" else 1.0,
            profiles_sample_rate=0.1 if environment == "production" else 1.0,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                SqlalchemyIntegration(),
                RedisIntegration(),
            ],
            # Performance monitoring
            enable_tracing=True,
            # Release tracking
            release=os.getenv("GIT_COMMIT", "unknown"),
            # Error sampling
            sample_rate=1.0,
            # Attach stack traces
            attach_stacktrace=True,
            # Send default PII (Personally Identifiable Information)
            send_default_pii=False,
            # Max breadcrumbs
            max_breadcrumbs=50,
            # Before send hook to filter sensitive data
            before_send=before_send_hook,
        )
        
        logger.info("sentry_initialized", environment=environment)
        return True
        
    except ImportError:
        logger.warning("sentry_sdk_not_installed", note="Install with: pip install sentry-sdk[fastapi]")
        return False
    except Exception as e:
        logger.error("sentry_initialization_failed", error=str(e))
        return False


def before_send_hook(event, hint):
    """
    Filter sensitive data before sending to Sentry.
    
    Args:
        event: Sentry event dictionary
        hint: Additional context
    
    Returns:
        Modified event or None to drop the event
    """
    # Remove sensitive headers
    if "request" in event and "headers" in event["request"]:
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        for header in sensitive_headers:
            if header in event["request"]["headers"]:
                event["request"]["headers"][header] = "[Filtered]"
    
    # Remove sensitive query parameters
    if "request" in event and "query_string" in event["request"]:
        sensitive_params = ["password", "token", "secret", "api_key"]
        query_string = event["request"]["query_string"]
        for param in sensitive_params:
            if param in query_string.lower():
                event["request"]["query_string"] = "[Filtered]"
                break
    
    return event


def capture_exception(error: Exception, context: Optional[dict] = None):
    """
    Capture an exception and send to Sentry.
    
    Args:
        error: Exception to capture
        context: Additional context dictionary
    """
    try:
        import sentry_sdk
        
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                sentry_sdk.capture_exception(error)
        else:
            sentry_sdk.capture_exception(error)
            
    except ImportError:
        logger.error("sentry_capture_failed", error=str(error), note="Sentry SDK not installed")
    except Exception as e:
        logger.error("sentry_capture_error", error=str(e))


def capture_message(message: str, level: str = "info", context: Optional[dict] = None):
    """
    Capture a message and send to Sentry.
    
    Args:
        message: Message to capture
        level: Severity level (debug, info, warning, error, fatal)
        context: Additional context dictionary
    """
    try:
        import sentry_sdk
        
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                sentry_sdk.capture_message(message, level=level)
        else:
            sentry_sdk.capture_message(message, level=level)
            
    except ImportError:
        logger.warning("sentry_message_failed", message=message, note="Sentry SDK not installed")
    except Exception as e:
        logger.error("sentry_message_error", error=str(e))

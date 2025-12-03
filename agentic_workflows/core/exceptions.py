"""Custom exceptions for Agentic Workflows."""
from typing import Optional, Dict, Any


class AgenticWorkflowsError(Exception):
    """Base exception for all Agentic Workflows errors."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }


# Workflow Errors
class WorkflowError(AgenticWorkflowsError):
    """Base class for workflow-related errors."""
    pass


class WorkflowNotFoundError(WorkflowError):
    """Workflow not found."""
    pass


class WorkflowValidationError(WorkflowError):
    """Workflow validation failed."""
    pass


class WorkflowExecutionError(WorkflowError):
    """Workflow execution failed."""
    pass


class WorkflowTimeoutError(WorkflowError):
    """Workflow execution timed out."""
    pass


class WorkflowCancelledError(WorkflowError):
    """Workflow was cancelled."""
    pass


# Task Errors
class TaskError(AgenticWorkflowsError):
    """Base class for task-related errors."""
    pass


class TaskNotFoundError(TaskError):
    """Task not found."""
    pass


class TaskValidationError(TaskError):
    """Task validation failed."""
    pass


class TaskExecutionError(TaskError):
    """Task execution failed."""
    pass


class TaskTimeoutError(TaskError):
    """Task execution timed out."""
    pass


class TaskRetryExhaustedError(TaskError):
    """Task retry attempts exhausted."""
    pass


# Plugin Errors
class PluginError(AgenticWorkflowsError):
    """Base class for plugin-related errors."""
    pass


class PluginNotFoundError(PluginError):
    """Plugin not found."""
    pass


class PluginLoadError(PluginError):
    """Failed to load plugin."""
    pass


class PluginExecutionError(PluginError):
    """Plugin execution failed."""
    pass


class PluginConfigurationError(PluginError):
    """Plugin configuration invalid."""
    pass


# Storage Errors
class StorageError(AgenticWorkflowsError):
    """Base class for storage-related errors."""
    pass


class StorageNotFoundError(StorageError):
    """Storage resource not found."""
    pass


class StoragePermissionError(StorageError):
    """Storage permission denied."""
    pass


class StorageQuotaExceededError(StorageError):
    """Storage quota exceeded."""
    pass


# Authentication & Authorization Errors
class AuthenticationError(AgenticWorkflowsError):
    """Authentication failed."""
    pass


class AuthorizationError(AgenticWorkflowsError):
    """Authorization failed - insufficient permissions."""
    pass


class TokenExpiredError(AuthenticationError):
    """Authentication token expired."""
    pass


# Configuration Errors
class ConfigurationError(AgenticWorkflowsError):
    """Configuration error."""
    pass


# API Errors
class APIError(AgenticWorkflowsError):
    """Base class for API-related errors."""
    pass


class RateLimitExceededError(APIError):
    """Rate limit exceeded."""
    pass


class InvalidRequestError(APIError):
    """Invalid API request."""
    pass


# Database Errors
class DatabaseError(AgenticWorkflowsError):
    """Database operation failed."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Database connection failed."""
    pass


# External Service Errors
class ExternalServiceError(AgenticWorkflowsError):
    """External service error."""
    pass


class ExternalServiceTimeoutError(ExternalServiceError):
    """External service timeout."""
    pass


class ExternalServiceUnavailableError(ExternalServiceError):
    """External service unavailable."""
    pass

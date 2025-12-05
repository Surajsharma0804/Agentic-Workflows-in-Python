"""Configuration management for Agentic Workflows."""
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "Agentic Workflows"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # API Server (FREE tier optimized)
    api_host: str = "0.0.0.0"
    api_port: int = 8000  # Render uses PORT env var
    api_workers: int = 1  # FREE tier: 1 worker only
    api_reload: bool = False
    
    # Security
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    # Database
    database_url: str = "sqlite:///./agentic_workflows.db"
    database_echo: bool = False
    
    # Redis (Optional - not available on FREE tier)
    redis_url: Optional[str] = None
    redis_max_connections: int = 10
    
    # Celery (Optional - not available on FREE tier)
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    celery_task_track_started: bool = False
    celery_task_time_limit: int = 1800  # 30 minutes (reduced for FREE tier)
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or console
    log_file: Optional[str] = None
    
    # Audit
    audit_log_path: str = "audit.log"
    audit_retention_days: int = 90
    
    # Workflow Execution (FREE tier optimized)
    max_concurrent_workflows: int = 5  # Reduced for FREE tier
    workflow_timeout_seconds: int = 1800  # 30 min max
    task_retry_max_attempts: int = 3
    task_retry_delay_seconds: int = 5
    
    # Storage
    storage_backend: str = "local"  # local, s3, azure, gcs
    storage_path: str = "./storage"
    
    # AWS (if using S3)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_s3_bucket: Optional[str] = None
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    openai_max_tokens: int = 4000
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    sentry_dsn: Optional[str] = None
    
    # CORS
    cors_origins: List[str] = ["*"]  # Allow all origins (frontend served from same domain)
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # Plugin System
    plugin_directory: str = "./plugins"
    plugin_auto_reload: bool = False
    
    # Workflow Versioning
    enable_versioning: bool = True
    max_versions_per_workflow: int = 10
    
    # Notifications
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    
    slack_webhook_url: Optional[str] = None
    
    # OAuth2 Providers
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: Optional[str] = None
    
    apple_client_id: Optional[str] = None
    apple_team_id: Optional[str] = None
    apple_key_id: Optional[str] = None
    apple_private_key: Optional[str] = None
    apple_redirect_uri: Optional[str] = None
    
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    github_redirect_uri: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix=""
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle single "*" or comma-separated list
            if v.strip() == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v if v else ["*"]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"
    
    def get_storage_path(self) -> Path:
        """Get storage path as Path object."""
        return Path(self.storage_path)
    
    def get_plugin_directory(self) -> Path:
        """Get plugin directory as Path object."""
        return Path(self.plugin_directory)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings

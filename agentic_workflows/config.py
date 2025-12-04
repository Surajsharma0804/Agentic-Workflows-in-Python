"""Configuration management for Agentic Workflows."""
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "Agentic Workflows"
    app_version: str = "1.0.0"
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API Server (FREE tier optimized)
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="PORT")  # Render uses PORT env var
    api_workers: int = Field(default=1, env="API_WORKERS")  # FREE tier: 1 worker only
    api_reload: bool = Field(default=False, env="API_RELOAD")
    
    # Security
    secret_key: str = Field(default="change-me-in-production", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = "HS256"
    
    # Database
    database_url: str = Field(
        default="sqlite:///./agentic_workflows.db",
        env="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis (Optional - not available on FREE tier)
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    redis_max_connections: int = Field(default=10, env="REDIS_MAX_CONNECTIONS")
    
    # Celery (Optional - not available on FREE tier)
    celery_broker_url: Optional[str] = Field(default=None, env="CELERY_BROKER_URL")
    celery_result_backend: Optional[str] = Field(default=None, env="CELERY_RESULT_BACKEND")
    celery_task_track_started: bool = False
    celery_task_time_limit: int = 1800  # 30 minutes (reduced for FREE tier)
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = "json"  # json or console
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Audit
    audit_log_path: str = Field(default="audit.log", env="AUDIT_LOG_PATH")
    audit_retention_days: int = Field(default=90, env="AUDIT_RETENTION_DAYS")
    
    # Workflow Execution (FREE tier optimized)
    max_concurrent_workflows: int = Field(default=5, env="MAX_CONCURRENT_WORKFLOWS")  # Reduced for FREE tier
    workflow_timeout_seconds: int = Field(default=1800, env="WORKFLOW_TIMEOUT_SECONDS")  # 30 min max
    task_retry_max_attempts: int = Field(default=3, env="TASK_RETRY_MAX_ATTEMPTS")
    task_retry_delay_seconds: int = Field(default=5, env="TASK_RETRY_DELAY_SECONDS")
    
    # Storage
    storage_backend: str = Field(default="local", env="STORAGE_BACKEND")  # local, s3, azure, gcs
    storage_path: str = Field(default="./storage", env="STORAGE_PATH")
    
    # AWS (if using S3)
    aws_access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_s3_bucket: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    
    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    openai_max_tokens: int = Field(default=4000, env="OPENAI_MAX_TOKENS")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["*"],  # Allow all origins (frontend served from same domain)
        env="CORS_ORIGINS"
    )
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Plugin System
    plugin_directory: str = Field(default="./plugins", env="PLUGIN_DIRECTORY")
    plugin_auto_reload: bool = Field(default=False, env="PLUGIN_AUTO_RELOAD")
    
    # Workflow Versioning
    enable_versioning: bool = Field(default=True, env="ENABLE_VERSIONING")
    max_versions_per_workflow: int = Field(default=10, env="MAX_VERSIONS_PER_WORKFLOW")
    
    # Notifications
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    smtp_from_email: Optional[str] = Field(default=None, env="SMTP_FROM_EMAIL")
    
    slack_webhook_url: Optional[str] = Field(default=None, env="SLACK_WEBHOOK_URL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
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

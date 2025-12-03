"""Configuration tests."""
import pytest
from agentic_workflows.config import Settings, get_settings

def test_settings_defaults():
    settings = Settings()
    assert settings.app_name == "Agentic Workflows"
    assert settings.environment == "development"
    assert settings.api_port == 8000

def test_get_settings():
    settings = get_settings()
    assert isinstance(settings, Settings)

def test_is_production():
    settings = Settings(environment="production")
    assert settings.is_production is True
    assert settings.is_development is False

def test_is_development():
    settings = Settings(environment="development")
    assert settings.is_development is True
    assert settings.is_production is False

"""LLM provider factory."""
from typing import Optional
import structlog

from .base import LLMProvider, LLMModel
from .openai_provider import OpenAIProvider
from .claude_provider import ClaudeProvider
from .dummy_provider import DummyProvider
from ..config import get_settings

logger = structlog.get_logger()
settings = get_settings()


def get_llm_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> LLMProvider:
    """
    Get LLM provider instance.
    
    Args:
        provider_name: Provider name (openai, claude, gemini, ollama, dummy)
        api_key: API key for the provider
        model: Model name to use
    
    Returns:
        LLMProvider instance
    """
    # Default to configured provider
    if provider_name is None:
        provider_name = getattr(settings, "llm_provider", "dummy")
    
    provider_name = provider_name.lower()
    
    # Get API key from settings if not provided
    if api_key is None:
        if provider_name == "openai":
            api_key = settings.openai_api_key
        elif provider_name == "claude":
            api_key = getattr(settings, "anthropic_api_key", None)
        elif provider_name == "gemini":
            api_key = getattr(settings, "google_api_key", None)
    
    # Create provider
    try:
        if provider_name == "openai":
            provider = OpenAIProvider(api_key=api_key, model=model or LLMModel.GPT4)
            if not provider.is_available():
                logger.warning("openai_not_available", reason="missing_api_key")
                return DummyProvider()
            return provider
        
        elif provider_name == "claude":
            provider = ClaudeProvider(api_key=api_key, model=model or LLMModel.CLAUDE3_SONNET)
            if not provider.is_available():
                logger.warning("claude_not_available", reason="missing_api_key")
                return DummyProvider()
            return provider
        
        elif provider_name == "dummy":
            return DummyProvider()
        
        else:
            logger.warning("unknown_provider", provider=provider_name)
            return DummyProvider()
    
    except Exception as e:
        logger.error("provider_creation_failed", provider=provider_name, error=str(e))
        return DummyProvider()

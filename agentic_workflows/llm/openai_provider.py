"""OpenAI LLM provider."""
from typing import Optional, Dict, Any, List
import structlog

from .base import LLMProvider, LLMResponse, LLMModel

logger = structlog.get_logger()


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = LLMModel.GPT4):
        super().__init__(api_key, model)
        self._client = None
    
    def _get_client(self):
        """Lazy load OpenAI client."""
        if self._client is None:
            try:
                import openai
                if self.api_key:
                    openai.api_key = self.api_key
                self._client = openai
            except ImportError:
                logger.warning("openai package not installed")
                return None
        return self._client
    
    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        client = self._get_client()
        return client is not None and self.api_key is not None
    
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using OpenAI."""
        messages = self.format_messages(prompt, system_prompt)
        return await self.chat(messages, temperature, max_tokens, **kwargs)
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate chat completion using OpenAI."""
        client = self._get_client()
        if not client:
            raise RuntimeError("OpenAI client not available")
        
        try:
            response = client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.default_temperature,
                max_tokens=max_tokens or self.default_max_tokens,
                **kwargs
            )
            
            choice = response.choices[0]
            
            return LLMResponse(
                content=choice.message.content,
                model=response.model,
                tokens_used=response.usage.total_tokens,
                finish_reason=choice.finish_reason,
                metadata={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }
            )
        except Exception as e:
            logger.error("openai_error", error=str(e))
            raise

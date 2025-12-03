"""Anthropic Claude LLM provider."""
from typing import Optional, Dict, Any, List
import structlog

from .base import LLMProvider, LLMResponse, LLMModel

logger = structlog.get_logger()


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = LLMModel.CLAUDE3_SONNET):
        super().__init__(api_key, model)
        self._client = None
    
    def _get_client(self):
        """Lazy load Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                if self.api_key:
                    self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("anthropic package not installed")
                return None
        return self._client
    
    def is_available(self) -> bool:
        """Check if Claude is available."""
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
        """Generate completion using Claude."""
        messages = self.format_messages(prompt, system_prompt)
        return await self.chat(messages, temperature, max_tokens, **kwargs)
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate chat completion using Claude."""
        client = self._get_client()
        if not client:
            raise RuntimeError("Claude client not available")
        
        try:
            # Extract system message if present
            system = None
            user_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.default_max_tokens,
                temperature=temperature or self.default_temperature,
                system=system,
                messages=user_messages,
                **kwargs
            )
            
            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                finish_reason=response.stop_reason,
                metadata={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                }
            )
        except Exception as e:
            logger.error("claude_error", error=str(e))
            raise

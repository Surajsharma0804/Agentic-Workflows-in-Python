"""OpenAI GPT integration plugin."""
from ..base import PluginBase
from typing import Optional
import openai
from ...config import get_settings

settings = get_settings()

class OpenAIPlugin(PluginBase):
    """OpenAI GPT plugin for AI-powered tasks."""
    
    name = "openai"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.api_key = params.get("api_key") or settings.openai_api_key
        self.model = params.get("model", settings.openai_model)
        self.prompt = params.get("prompt")
        self.max_tokens = params.get("max_tokens", settings.openai_max_tokens)
        self.temperature = params.get("temperature", 0.7)
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def plan(self) -> list:
        return [{"action": "openai_completion", "model": self.model, "prompt_length": len(self.prompt or "")}]
    
    def execute(self) -> dict:
        if not self.api_key:
            return {"status": "error", "message": "OpenAI API key not configured"}
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": self.prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            result = response.choices[0].message.content
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens
                })
            
            return {
                "status": "ok",
                "result": result,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

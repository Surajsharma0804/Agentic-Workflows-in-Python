"""Base agent class."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import structlog

from ..llm import LLMProvider, get_llm_provider
from ..core.audit import AuditLog

logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all AI agents."""
    
    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        audit: Optional[AuditLog] = None
    ):
        self.llm = llm_provider or get_llm_provider()
        self.audit = audit or AuditLog()
        self.agent_name = self.__class__.__name__
    
    def log_action(self, action: str, **kwargs):
        """Log agent action."""
        logger.info(
            "agent_action",
            agent=self.agent_name,
            action=action,
            **kwargs
        )
        if self.audit:
            self.audit.record({
                "agent": self.agent_name,
                "action": action,
                **kwargs
            })
    
    async def think(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Use LLM to think about a problem."""
        self.log_action("thinking", prompt_length=len(prompt))
        
        try:
            response = await self.llm.complete(
                prompt=prompt,
                system_prompt=system_prompt or self.get_system_prompt()
            )
            
            self.log_action(
                "thought_complete",
                tokens_used=response.tokens_used,
                model=response.model
            )
            
            return response.content
        except Exception as e:
            logger.error("thinking_failed", agent=self.agent_name, error=str(e))
            return self.fallback_response(prompt)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent."""
        pass
    
    @abstractmethod
    def fallback_response(self, prompt: str) -> str:
        """Fallback response when LLM fails."""
        pass

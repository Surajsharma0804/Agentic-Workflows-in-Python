"""Dummy LLM provider for offline mode and testing."""
from typing import Optional, Dict, Any, List
import random

from .base import LLMProvider, LLMResponse, LLMModel


class DummyProvider(LLMProvider):
    """Dummy provider that returns simulated responses."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = LLMModel.DUMMY):
        super().__init__(api_key, model)
    
    def is_available(self) -> bool:
        """Dummy provider is always available."""
        return True
    
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate dummy completion."""
        # Simulate intelligent response based on prompt keywords
        response_content = self._generate_dummy_response(prompt)
        
        return LLMResponse(
            content=response_content,
            model=self.model,
            tokens_used=random.randint(50, 200),
            finish_reason="stop",
            metadata={"provider": "dummy", "simulated": True}
        )
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate dummy chat completion."""
        last_message = messages[-1]["content"] if messages else ""
        return await self.complete(last_message, temperature=temperature, max_tokens=max_tokens)
    
    def _generate_dummy_response(self, prompt: str) -> str:
        """Generate contextual dummy response."""
        prompt_lower = prompt.lower()
        
        # Workflow planning responses
        if "plan" in prompt_lower or "workflow" in prompt_lower:
            return """Based on the workflow specification, I recommend the following execution plan:

1. **Validation Phase**: Validate all input parameters and check dependencies
2. **Preparation Phase**: Set up required resources and connections
3. **Execution Phase**: Execute tasks in optimal order with parallelization where possible
4. **Verification Phase**: Verify outputs and check for errors
5. **Cleanup Phase**: Release resources and finalize results

This plan ensures safe, efficient execution with proper error handling."""
        
        # Error recovery responses
        elif "error" in prompt_lower or "failed" in prompt_lower or "fix" in prompt_lower:
            return """I've analyzed the error and suggest the following recovery steps:

1. **Root Cause**: The task failed due to [simulated analysis]
2. **Immediate Fix**: Retry with adjusted parameters
3. **Prevention**: Add validation checks before execution
4. **Alternative**: Consider using a different approach if retry fails

Would you like me to attempt automatic recovery?"""
        
        # Validation responses
        elif "validate" in prompt_lower or "check" in prompt_lower:
            return """Validation complete. The workflow specification appears valid with the following notes:

✓ All required fields are present
✓ Task dependencies are properly defined
✓ Plugin configurations are correct
⚠ Consider adding timeout values for long-running tasks
⚠ Recommend adding retry logic for network operations

Overall: Ready for execution"""
        
        # Optimization responses
        elif "optimize" in prompt_lower or "improve" in prompt_lower:
            return """I've identified several optimization opportunities:

1. **Parallelization**: Tasks A and B can run concurrently
2. **Caching**: Enable caching for repeated operations
3. **Resource Usage**: Reduce memory footprint by streaming large files
4. **Performance**: Use async operations for I/O-bound tasks

Estimated improvement: 40% faster execution"""
        
        # Default response
        else:
            return f"""I understand you're asking about: "{prompt[:100]}..."

As an AI assistant, I can help with:
- Workflow planning and optimization
- Error analysis and recovery suggestions
- Specification validation
- Best practices recommendations

How can I assist you further?"""

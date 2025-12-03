"""Safe shell command execution plugin."""
from typing import Dict, Any, List
import subprocess
import shlex
import structlog

from ..base import PluginBase

logger = structlog.get_logger()


class ShellCommandPlugin(PluginBase):
    """
    Safe shell command execution.
    
    Features:
    - Whitelist of allowed commands
    - Timeout protection
    - Output capture
    - Non-destructive by default
    """
    
    name = "shell_command"
    
    # Whitelist of safe commands
    SAFE_COMMANDS = {
        "ls", "dir", "pwd", "echo", "cat", "head", "tail",
        "grep", "find", "wc", "sort", "uniq", "date",
        "git", "python", "node", "npm", "pip"
    }
    
    def __init__(self, params: Dict[str, Any], audit=None):
        super().__init__(params, audit=audit)
        self.command = params.get("command")
        self.args = params.get("args", [])
        self.cwd = params.get("cwd", ".")
        self.timeout = params.get("timeout", 30)
        self.allow_unsafe = params.get("allow_unsafe", False)
        self.capture_output = params.get("capture_output", True)
    
    def plan(self) -> List[Dict[str, Any]]:
        return [{
            "action": "shell_command",
            "command": self.command,
            "args": self.args,
            "safe": self._is_safe_command()
        }]
    
    def execute(self) -> Dict[str, Any]:
        """Execute shell command safely."""
        try:
            # Safety check
            if not self.allow_unsafe and not self._is_safe_command():
                return {
                    "status": "error",
                    "message": f"Command '{self.command}' not in safe list. Set allow_unsafe=true to override."
                }
            
            # Build command
            cmd = [self.command] + self.args
            
            # Execute
            result = subprocess.run(
                cmd,
                cwd=self.cwd,
                timeout=self.timeout,
                capture_output=self.capture_output,
                text=True
            )
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "command": self.command,
                    "return_code": result.returncode
                })
            
            return {
                "status": "ok" if result.returncode == 0 else "error",
                "return_code": result.returncode,
                "stdout": result.stdout if self.capture_output else None,
                "stderr": result.stderr if self.capture_output else None
            }
        
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": f"Command timed out after {self.timeout} seconds"
            }
        except Exception as e:
            logger.error("shell_command_failed", error=str(e))
            return {"status": "error", "message": str(e)}
    
    def _is_safe_command(self) -> bool:
        """Check if command is in safe list."""
        return self.command in self.SAFE_COMMANDS

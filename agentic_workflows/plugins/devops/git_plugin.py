"""Git operations plugin."""
from ..base import PluginBase
import subprocess
from pathlib import Path

class GitPlugin(PluginBase):
    """Git version control operations."""
    
    name = "git"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.repo_path = params.get("repo_path", ".")
        self.operation = params.get("operation")  # clone, pull, push, commit, status
        self.remote_url = params.get("remote_url")
        self.branch = params.get("branch", "main")
        self.commit_message = params.get("commit_message")
    
    def plan(self) -> list:
        return [{"action": f"git_{self.operation}", "repo": self.repo_path}]
    
    def execute(self) -> dict:
        try:
            if self.operation == "clone":
                result = subprocess.run(
                    ["git", "clone", self.remote_url, self.repo_path],
                    capture_output=True, text=True
                )
            
            elif self.operation == "pull":
                result = subprocess.run(
                    ["git", "-C", self.repo_path, "pull", "origin", self.branch],
                    capture_output=True, text=True
                )
            
            elif self.operation == "commit":
                subprocess.run(["git", "-C", self.repo_path, "add", "."])
                result = subprocess.run(
                    ["git", "-C", self.repo_path, "commit", "-m", self.commit_message],
                    capture_output=True, text=True
                )
            
            elif self.operation == "push":
                result = subprocess.run(
                    ["git", "-C", self.repo_path, "push", "origin", self.branch],
                    capture_output=True, text=True
                )
            
            elif self.operation == "status":
                result = subprocess.run(
                    ["git", "-C", self.repo_path, "status"],
                    capture_output=True, text=True
                )
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "operation": self.operation,
                    "repo": self.repo_path
                })
            
            return {
                "status": "ok" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

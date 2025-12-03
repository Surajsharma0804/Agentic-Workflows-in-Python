"""Slack integration plugin."""
from ..base import PluginBase
import requests

class SlackPlugin(PluginBase):
    """Slack notifications and messaging."""
    
    name = "slack"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.webhook_url = params.get("webhook_url")
        self.channel = params.get("channel")
        self.message = params.get("message")
        self.username = params.get("username", "Agentic Workflows")
        self.icon_emoji = params.get("icon_emoji", ":robot_face:")
    
    def plan(self) -> list:
        return [{"action": "slack_message", "channel": self.channel}]
    
    def execute(self) -> dict:
        try:
            payload = {
                "channel": self.channel,
                "username": self.username,
                "text": self.message,
                "icon_emoji": self.icon_emoji
            }
            
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "channel": self.channel
                })
            
            return {"status": "ok", "message": "Sent to Slack"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

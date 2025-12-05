from .base import PluginBase
import requests

class HTTPTask(PluginBase):
    name = "http_task"

    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.url = params.get("url")
        self.method = params.get("method", "GET").upper()
        self.payload = params.get("payload")
        self.headers = params.get("headers", {})
        self.timeout = float(params.get("timeout", 10))
        self.dry_run = params.get("dry_run", True)

    def plan(self):
        return [{"action": "http_call", "method": self.method, "url": self.url}]

    def execute(self):
        """Execute HTTP request with rich response details."""
        if self.dry_run:
            return {
                "status": "planned",
                "method": self.method,
                "url": self.url,
                "headers": self.headers,
                "has_payload": self.payload is not None,
                "timeout": self.timeout
            }
        
        try:
            resp = requests.request(
                self.method,
                self.url,
                json=self.payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Extract response details
            response_data = {
                "status": "completed",
                "status_code": resp.status_code,
                "reason": resp.reason,
                "url": resp.url,
                "method": self.method,
                "response_size_bytes": len(resp.content),
                "response_headers": dict(resp.headers),
                "elapsed_seconds": resp.elapsed.total_seconds(),
                "encoding": resp.encoding
            }
            
            # Add response body preview (limit size)
            if resp.text:
                response_data["response_preview"] = resp.text[:500]  # First 500 chars
                response_data["response_full_length"] = len(resp.text)
            
            # Try to parse JSON if applicable
            if "application/json" in resp.headers.get("Content-Type", ""):
                try:
                    response_data["response_json"] = resp.json()
                except:
                    pass
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "status_code": resp.status_code,
                    "url": self.url,
                    "method": self.method,
                    "elapsed": resp.elapsed.total_seconds()
                })
            
            return response_data
            
        except requests.exceptions.Timeout:
            return {
                "status": "failed",
                "error": "Request timeout",
                "url": self.url,
                "timeout": self.timeout
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "url": self.url,
                "method": self.method
            }

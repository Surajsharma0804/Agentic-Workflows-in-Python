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
        if self.dry_run:
            return {"status": "planned", "url": self.url}
        resp = requests.request(self.method, self.url, json=self.payload, headers=self.headers, timeout=self.timeout)
        if self.audit:
            self.audit.record({"plugin": self.name, "status_code": resp.status_code, "url": self.url})
        return {"status": "ok", "status_code": resp.status_code, "text_len": len(resp.text)}

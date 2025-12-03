# Plugin Development Guide

## Creating a Custom Plugin

### 1. Create Plugin Class

```python
from agentic_workflows.plugins.base import PluginBase

class MyPlugin(PluginBase):
    name = "my_plugin"
    
    def __init__(self, params: dict, audit=None):
        super().__init__(params, audit=audit)
        self.my_param = params.get("my_param")
    
    def plan(self) -> list:
        return [{"action": "my_action", "param": self.my_param}]
    
    def execute(self) -> dict:
        # Your implementation
        result = do_something(self.my_param)
        
        if self.audit:
            self.audit.record({"plugin": self.name, "result": result})
        
        return {"status": "ok", "result": result}
```

### 2. Register Plugin

Add to `agentic_workflows/core/agents.py`:

```python
PLUGIN_REGISTRY = {
    "my_plugin": "agentic_workflows.plugins.my_plugin.MyPlugin",
    # ... other plugins
}
```

### 3. Use in Workflow

```yaml
id: my-workflow
name: My Workflow
tasks:
  - id: task1
    type: my_plugin
    params:
      my_param: "value"
```

## Available Plugins

### Built-in
- `file_organizer` - File organization
- `email_summarizer` - Email summarization
- `http_task` - HTTP requests

### AI
- `openai` - OpenAI GPT integration

### Database
- `postgresql` - PostgreSQL operations

### Cloud
- `aws_s3` - AWS S3 storage

### Communication
- `slack` - Slack notifications
- `email` - Email sending

### DevOps
- `git` - Git operations

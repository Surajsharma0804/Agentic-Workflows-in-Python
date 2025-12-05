# API Usage Guide

Complete guide for using the Agentic Workflows API.

## Base URL
```
Production: https://agentic-workflows-pm7o.onrender.com
Local: http://localhost:8000
```

## Authentication

Most endpoints require authentication. Include the JWT token in the Authorization header:

```bash
Authorization: Bearer <your_token>
```

### Register a New User
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe"
  }
}
```

## Plugins API

### List All Plugins
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/plugins
```

Response:
```json
[
  {
    "id": "file_organizer",
    "name": "File Organizer",
    "version": "1.0.0",
    "description": "Organize files by type, date, or custom rules",
    "category": "File Management",
    "enabled": true,
    "parameters": {
      "source_dir": {
        "type": "string",
        "required": true,
        "description": "Source directory path"
      }
    }
  }
]
```

### Get Plugin Details
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/plugins/file_organizer
```

### Test Plugin (Dry Run)
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/plugins/file_organizer/test \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "source_dir": "/path/to/files",
      "organize_by": "type"
    }
  }'
```

Response:
```json
{
  "status": "success",
  "plan": [
    {
      "action": "scan",
      "target": "/path/to/files"
    },
    {
      "action": "organize",
      "by": "type"
    }
  ]
}
```

### Execute Plugin
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/plugins/http_task/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "url": "https://api.github.com/users/octocat",
      "method": "GET"
    }
  }'
```

## AI & LLM API

### Chat with AI Assistant
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I create a workflow that organizes files?",
    "context": {
      "current_page": "workflows"
    }
  }'
```

Response:
```json
{
  "status": "success",
  "response": "To create a file organization workflow, you can use the file_organizer plugin...",
  "provider": "dummy"
}
```

### Generate Workflow from Description
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/llm/generate-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Create a workflow that fetches data from an API and organizes downloaded files"
  }'
```

Response:
```json
{
  "status": "success",
  "workflow": {
    "name": "API Data Fetcher",
    "description": "Fetch data and organize files",
    "tasks": [
      {
        "id": "fetch_data",
        "type": "http_task",
        "params": {
          "url": "https://api.example.com/data",
          "method": "GET"
        }
      },
      {
        "id": "organize_files",
        "type": "file_organizer",
        "params": {
          "source_dir": "./downloads"
        },
        "depends_on": ["fetch_data"]
      }
    ]
  }
}
```

### List LLM Providers
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/llm/providers
```

## Workflows API

### Create Workflow
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/workflows \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily File Cleanup",
    "description": "Organize files daily",
    "spec": "name: Daily Cleanup\ntasks:\n  - id: cleanup\n    type: file_organizer\n    params:\n      source_dir: ./downloads"
  }'
```

### List Workflows
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/workflows \
  -H "Authorization: Bearer <token>"
```

### Get Workflow
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/workflows/1 \
  -H "Authorization: Bearer <token>"
```

### Execute Workflow
```bash
curl -X POST https://agentic-workflows-pm7o.onrender.com/api/workflows/1/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "source_dir": "./my-files"
    }
  }'
```

Response:
```json
{
  "status": "success",
  "execution_id": 123,
  "message": "Workflow execution started"
}
```

### Get Execution Status
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/executions/123 \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "id": 123,
  "workflow_id": 1,
  "status": "completed",
  "started_at": "2025-12-05T10:00:00Z",
  "completed_at": "2025-12-05T10:05:00Z",
  "result": {
    "files_organized": 42,
    "errors": 0
  }
}
```

## Audit Logs API

### List Audit Logs
```bash
curl "https://agentic-workflows-pm7o.onrender.com/api/audit/logs?limit=10" \
  -H "Authorization: Bearer <token>"
```

### Filter Audit Logs
```bash
curl "https://agentic-workflows-pm7o.onrender.com/api/audit/logs?action=workflow.execute&resource_type=workflow" \
  -H "Authorization: Bearer <token>"
```

### Get Audit Statistics
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/audit/stats \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "total_logs": 1234,
  "by_action": {
    "workflow.create": 45,
    "workflow.execute": 789,
    "workflow.delete": 12
  },
  "by_user": {
    "user@example.com": 856
  }
}
```

## Health Check

### Check System Health
```bash
curl https://agentic-workflows-pm7o.onrender.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

Currently no rate limiting is enforced, but it's recommended to:
- Limit workflow executions to 10 per minute
- Limit API calls to 100 per minute
- Use pagination for large result sets

## Best Practices

1. **Always use HTTPS** in production
2. **Store tokens securely** - never commit them to git
3. **Use pagination** for list endpoints
4. **Handle errors gracefully** - check status codes
5. **Test plugins** before executing them
6. **Monitor audit logs** for security
7. **Use AI features** for workflow optimization

## Examples

### Complete Workflow Creation Flow

```bash
# 1. Register/Login
TOKEN=$(curl -X POST https://agentic-workflows-pm7o.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass"}' \
  | jq -r '.access_token')

# 2. Generate workflow with AI
WORKFLOW=$(curl -X POST https://agentic-workflows-pm7o.onrender.com/api/llm/generate-workflow \
  -H "Content-Type: application/json" \
  -d '{"description":"Organize my downloads folder"}' \
  | jq -r '.workflow')

# 3. Create workflow
WORKFLOW_ID=$(curl -X POST https://agentic-workflows-pm7o.onrender.com/api/workflows \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Auto Organizer\",\"spec\":\"$WORKFLOW\"}" \
  | jq -r '.id')

# 4. Execute workflow
EXECUTION_ID=$(curl -X POST https://agentic-workflows-pm7o.onrender.com/api/workflows/$WORKFLOW_ID/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq -r '.execution_id')

# 5. Check status
curl https://agentic-workflows-pm7o.onrender.com/api/executions/$EXECUTION_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Support

For issues or questions:
- GitHub: https://github.com/Surajsharma0804/Agentic-Workflows-in-Python
- API Docs: https://agentic-workflows-pm7o.onrender.com/api/docs

# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints (except health checks) require JWT authentication.

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Use token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/workflows/
```

## Endpoints

### Health Checks
- `GET /api/health` - Health status
- `GET /api/ready` - Readiness check
- `GET /api/live` - Liveness check

### Workflows
- `GET /api/workflows/` - List all workflows
- `POST /api/workflows/` - Create workflow
- `GET /api/workflows/{id}` - Get workflow
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

### Tasks
- `GET /api/tasks/` - List all tasks
- `GET /api/tasks/{id}` - Get task details

### Plugins
- `GET /api/plugins/` - List available plugins
- `GET /api/plugins/{name}` - Get plugin details

## Interactive Documentation
Visit http://localhost:8000/api/docs for Swagger UI

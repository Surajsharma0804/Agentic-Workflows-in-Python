# Deployment Guide

## Docker Deployment

### Build Image
```bash
docker build -t agentic-workflows:latest .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3 (optional)

### Deploy
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secret.yaml

# Deploy application
kubectl apply -f k8s/

# Check status
kubectl get pods -n agentic-workflows
```

### Scale
```bash
kubectl scale deployment agentic-workflows-api --replicas=5 -n agentic-workflows
```

## Cloud Platforms

### AWS ECS
See `docs/deploy/aws-ecs.md`

### Azure AKS
See `docs/deploy/azure-aks.md`

### GCP GKE
See `docs/deploy/gcp-gke.md`

## Monitoring

### Prometheus
Metrics available at `:9090/metrics`

### Grafana
Import dashboards from `monitoring/grafana/`

### Logs
Structured JSON logs to stdout

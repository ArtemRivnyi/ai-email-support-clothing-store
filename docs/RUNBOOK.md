# Operational Runbook: AI Email Support System

## 1. System Overview
The AI Email Support System automates customer support for a clothing store. It fetches emails from Gmail, classifies them using a local LLM (Ollama), searches a Knowledge Base (FAISS), and generates replies.

### Components
- **API**: Flask application for health checks and metrics.
- **Worker**: Background process (RQ) handling email logic.
- **Redis**: Message broker and cache.
- **Ollama**: Local LLM inference engine.
- **Dashboard**: Streamlit admin interface.

## 2. Deployment
### Prerequisites
- Kubernetes Cluster (v1.24+)
- `kubectl` configured
- Secrets (Gmail Token, etc.) prepared

### Steps
1. **Apply Secrets**:
   ```bash
   kubectl apply -f k8s/namespace.yml
   kubectl apply -f k8s/secrets.yml
   ```
2. **Deploy Services**:
   ```bash
   kubectl apply -f k8s/
   ```
3. **Verify**:
   ```bash
   kubectl get pods -n ai-email-support
   ```

## 3. Monitoring & Alerts
### Key Metrics (Prometheus/Grafana)
- **Queue Size** (`email_queue_size`): Should be < 50. Alert if > 100 for 10m.
- **Processing Time** (`email_processing_seconds`): Target < 5s. Alert if p95 > 10s.
- **Success Rate**: Target > 95%. Alert if < 90%.

### Dashboards
- **Grafana**: `http://<ingress-host>/` (or port-forward 3000)
- **Admin Dashboard**: `http://<ingress-host>/` (or port-forward 8501)

## 4. Common Issues & Troubleshooting

### Issue: Queue Size Growing
**Symptoms**: `email_queue_size` metric increasing, customers complaining of delays.
**Diagnosis**:
1. Check worker logs: `kubectl logs -l app=worker -n ai-email-support`
2. Check Ollama load: Is inference slow?
**Resolution**:
- Scale workers: `kubectl scale deployment worker --replicas=5 -n ai-email-support`
- Restart stuck workers: `kubectl rollout restart deployment worker -n ai-email-support`

### Issue: LLM Errors / "Ollama connection failed"
**Symptoms**: Logs show `ConnectionError` to Ollama.
**Resolution**:
1. Check Ollama pod status: `kubectl get pods -l app=ollama`
2. Restart Ollama: `kubectl rollout restart deployment ollama`
3. Verify resource limits (OOMKilled?).

### Issue: Gmail Token Expired
**Symptoms**: Logs show `RefreshError` or `invalid_grant`.
**Resolution**:
1. Run local auth script to generate new `token.pickle`.
2. Update K8s secret:
   ```bash
   kubectl create secret generic app-secrets --from-file=token.pickle --dry-run=client -o yaml | kubectl apply -f -
   ```
3. Restart workers.

## 5. Backup & Recovery
- **Redis**: Persistence is enabled via PVC. Backup the volume snapshot daily.
- **Knowledge Base**: The `embeddings/` directory is rebuilt on startup if missing, but backing up `documents.pkl` is recommended.

## 6. Security
- **Secrets**: Rotate Google Client Secrets annually.
- **Access**: Restrict Dashboard access via Ingress/VPN.

# Production Launch Checklist

## Infrastructure
- [ ] **Kubernetes Cluster**: Healthy and running version 1.24+.
- [ ] **Resources**: Node capacity sufficient for Ollama (min 4GB RAM per replica).
- [ ] **Storage**: PVCs bound for Redis and Ollama.
- [ ] **Network**: Ingress controller installed and LoadBalancer IP assigned.

## Security
- [ ] **Secrets**: All sensitive env vars moved to K8s Secrets.
- [ ] **SSL/TLS**: Cert-manager configured, valid HTTPS certificate for domain.
- [ ] **Firewall**: Redis and Ollama ports NOT exposed publicly.
- [ ] **Rate Limiting**: Enabled and tested (200/day).

## Application
- [ ] **Ollama Models**: `gemma:7b` (or chosen model) pulled and verified.
- [ ] **Knowledge Base**: Initial FAQs loaded and indexed.
- [ ] **Gmail Auth**: Valid `token.pickle` generated and mounted.

## Monitoring
- [ ] **Prometheus**: Scraping API and Worker targets.
- [ ] **Grafana**: Dashboards imported and showing data.
- [ ] **Alerts**: Notification channels (Slack/Email) configured for critical alerts.

## Testing
- [ ] **Load Test**: System handles 10 concurrent emails without crashing.
- [ ] **Recovery**: Restarting Redis/Worker doesn't lose data.
- [ ] **Accuracy**: Verified random sample of 20 responses.

## Sign-off
- [ ] **DevOps**: Infrastructure ready.
- [ ] **Security**: Audit passed.
- [ ] **Product Owner**: Go/No-Go decision.

# 🚀 AI Email Support System

![CI/CD](https://github.com/artemrivnyi/ai-email/actions/workflows/ci-cd.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

A production-ready AI-powered email support agent for clothing stores. It automatically classifies incoming emails, searches a knowledge base (RAG), and drafts responses using a local LLM (Ollama).

## ✨ Features

- **🤖 Local LLM**: Uses Ollama (Gemma:7b) for privacy-first, cost-effective inference.
- **📚 RAG Architecture**: Retrieval-Augmented Generation using FAISS for accurate, context-aware answers.
- **⚡ Async Processing**: Redis Queue (RQ) handles high volumes of emails asynchronously.
- **🛡️ Security**: Rate limiting, OAuth auto-refresh, and centralized secret management.
- **📊 Admin Dashboard**: Streamlit UI for monitoring, analytics, and knowledge base management.
- **☸️ Kubernetes Ready**: Full set of manifests for scalable deployment.
- **📈 Observability**: Prometheus metrics and Grafana dashboards included.

## 🏗️ Architecture

The system follows a microservices-ready architecture:

- **API**: Flask application handling health checks and metrics.
- **Worker**: Background process that fetches emails, runs RAG pipeline, and sends replies.
- **Redis**: Message broker for the job queue and caching layer.
- **Ollama**: Local inference engine.
- **Dashboard**: Admin interface.

See [Architecture Documentation](docs/architecture/c4-container.md) for detailed diagrams.

## 🚀 Quick Start (Docker Compose)

1. **Prerequisites**: Docker & Docker Compose installed.
2. **Configuration**:
   Copy `.env.example` to `.env` and fill in your Google Credentials.
   ```bash
   cp .env.example .env
   ```
3. **Run**:
   ```bash
   docker-compose -f docker-compose.production.yml up -d --build
   ```
4. **Access**:
   - **Dashboard**: [http://localhost:8501](http://localhost:8501)
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (admin/admin)
   - **API Health**: [http://localhost:5000/health](http://localhost:5000/health)

## ☸️ Production Deployment (Kubernetes)

1. **Setup Secrets**:
   Edit `k8s/secrets.yml` with your base64 encoded credentials.
2. **Deploy**:
   ```bash
   kubectl apply -f k8s/namespace.yml
   kubectl apply -f k8s/secrets.yml
   kubectl apply -f k8s/
   ```
3. **Verify**:
   ```bash
   kubectl get pods -n ai-email-support
   ```

See [Runbook](docs/RUNBOOK.md) for detailed operational procedures.

## 🛠️ Development

### Project Structure
```
.
├── api/                # Flask API
├── auth/               # OAuth & Auth logic
├── config/             # Configuration & Secrets
├── dashboard/          # Streamlit Admin UI
├── docs/               # Documentation & Diagrams
├── k8s/                # Kubernetes Manifests
├── middleware/         # API Middleware (Rate Limiting)
├── monitoring/         # Prometheus & Grafana configs
├── services/           # Core Logic (Gmail, LLM, RAG)
├── tests/              # Unit & Integration Tests
├── utils/              # Shared Utilities (Logging)
├── worker.py           # Background Worker Entrypoint
└── docker-compose.production.yml
```

### Running Tests
```bash
pip install -r requirements.txt
pytest tests/
```

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

# 🤖 AI Email Support System

![CI Status](https://github.com/ArtemRivnyi/ai-email-support-clothing-store/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5.svg)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**An enterprise-grade, privacy-first AI email automation platform designed for e-commerce.**

This system autonomously processes incoming customer support emails, classifies them using local LLMs (Ollama), retrieves relevant policies via RAG (Retrieval-Augmented Generation), and drafts professional responses—all without data leaving your infrastructure.

---

## 📸 Dashboard Preview

![Admin Dashboard](docs/images/dashboard-preview.png)

*Real-time monitoring of email processing, queue status, and system health.*

---

## 🏗️ Architecture

The system is built on a robust microservices architecture, ensuring scalability and fault tolerance.

```mermaid
C4Container
    title Container Diagram for AI Email Support System

    Person(customer, "Customer", "Sends emails")
    Person(admin, "Admin", "Uses Dashboard")

    System_Ext(gmail, "Gmail API", "Email Service")

    Container_Boundary(c1, "AI Email Support System") {
        Container(api, "API Service", "Python/Flask", "Handles HTTP requests, health checks, metrics")
        Container(worker, "Worker Service", "Python/RQ", "Processes emails asynchronously")
        Container(dashboard, "Admin Dashboard", "Streamlit", "UI for management and analytics")
        ContainerDb(redis, "Redis", "Redis 7", "Message Broker & Cache")
        ContainerDb(ollama, "Ollama", "Local LLM", "Inference Engine (Gemma:7b)")
    }

    Rel(customer, gmail, "Sends email")
    Rel(worker, gmail, "Fetches emails / Sends replies")
    
    Rel(worker, redis, "Consumes jobs / Caches data")
    Rel(api, redis, "Checks health / Metrics")
    Rel(dashboard, redis, "Reads metrics / Manages Queue")
    
    Rel(worker, ollama, "Generates Embeddings & Answers")
    Rel(dashboard, api, "Uses API")
    
    Rel(admin, dashboard, "Views")
```

---

## ✨ Key Features

*   **🚀 Microservices Architecture**: Decoupled services (API, Worker, Dashboard) containerized with Docker.
*   **🧠 Privacy-First AI**: Uses **Ollama** running locally (Gemma:7b) for classification and generation. No data sent to external AI providers.
*   **📚 RAG Engine**: Retrieval-Augmented Generation using **FAISS** vector search to answer questions based on your specific knowledge base.
*   **⚡ Asynchronous Processing**: **Redis Queue (RQ)** handles high volumes of emails without blocking.
*   **🛡️ Enterprise Security**:
    *   OAuth2 Gmail integration.
    *   Rate limiting on API endpoints.
    *   Secure environment variable management.
    *   `bandit` security scanning in CI/CD.
*   **📊 Observability**:
    *   **Prometheus** metrics exposure.
    *   **Grafana** dashboards (ready-to-use).
    *   **Streamlit** admin interface for real-time control.
*   **☸️ Cloud-Ready**: Includes full **Kubernetes** manifests for deployment on AWS, GCP, or DigitalOcean.

---

## 🚀 Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/ArtemRivnyi/ai-email-support-clothing-store.git
cd ai-email-support-clothing-store
```

### 2. Configure Environment
Create a `.env` file (or use the provided `docker-compose.production.yml` defaults):
```bash
cp .env.example .env
# Edit .env with your Gmail credentials if running locally without Docker secrets
```

### 3. Run with Docker Compose
```bash
docker-compose -f docker-compose.production.yml up --build -d
```

The system will start the following services:
*   **API**: `http://localhost:5000`
*   **Dashboard**: `http://localhost:8501`
*   **Ollama**: `http://localhost:11434`
*   **Redis**: `localhost:6379`

---

## 📂 Project Structure

```
├── api/                # Flask API service
├── config/             # Configuration & Secrets management
├── dashboard/          # Streamlit Admin Dashboard
├── docs/               # Documentation (Architecture, Runbooks)
├── embeddings/         # FAISS vector store & Knowledge Base
├── k8s/                # Kubernetes manifests
├── services/           # Core business logic (LLM, RAG, Gmail)
├── tests/              # Unit & Integration tests
├── worker.py           # Background task worker
└── docker-compose.production.yml
```

---

## 📚 Documentation

*   [Value Proposition & ROI](docs/VALUE_PROPOSITION.md)
*   [Operational Runbook](docs/RUNBOOK.md)
*   [Production Checklist](docs/PRODUCTION_CHECKLIST.md)
*   [Demo Script](docs/DEMO_SCRIPT.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ by Artem Rivnyi*

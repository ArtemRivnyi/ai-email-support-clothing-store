
   ```bash
   cp .env.example .env
   ```
3. **Run**:
   ```bash
   docker-compose -f docker-compose.production.yml up -d --build
   ```
4. **Access**:
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

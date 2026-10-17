# Contributing to AI Email Support System

Thank you for contributing to this AI platform!

## 🚀 Development Guidelines

1. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. For Kubernetes & Infrastructure contributions:
   * Helm templates must pass `helm lint helm/`
   * Terraform configs must be formatted with `terraform fmt -check`
3. Run test suites:
   ```bash
   pytest tests/ -v
   ```

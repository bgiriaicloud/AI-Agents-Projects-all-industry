# 🚀 Healthcare Agent Deployment Guide

This guide ensures your Healthcare AI Agent is deployed with **HIPAA-compliant** considerations and high availability.

## 🛠️ Prerequisites
- Python 3.10+
- Docker & Docker Compose
- API Keys: OpenAI / Google Gemini / Pinecone

## 📦 Containerization (Docker)

Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## ☁️ Cloud Deployment (GCP Cloud Run)

1.  **Build Image:** `gcloud builds submit --tag gcr.io/PROJECT_ID/healthcare-agent`
2.  **Deploy:** `gcloud run deploy healthcare-agent --image gcr.io/PROJECT_ID/healthcare-agent --platform managed`

## 🔒 Security Best Practices
1.  **Data Masking**: Ensure PII (Personally Identifiable Information) is scrubbed before sending data to LLMs.
2.  **Encryption**: Use TLS for all data in transit.
3.  **Audit Logs**: Log every agent action for regulatory compliance.

## 🧪 Quick Test
```bash
# Run local dev server
pip install -r requirements.txt
streamlit run healthcare_agent.py
```

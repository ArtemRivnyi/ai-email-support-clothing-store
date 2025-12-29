from flask import Flask, jsonify
from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os
import redis
import requests

from middleware.rate_limiter import init_rate_limiter

app = Flask(__name__)
limiter = init_rate_limiter(app)

# Metrics
EMAILS_PROCESSED = Counter('emails_processed_total', 'Total emails processed', ['status'])
PROCESSING_TIME = Histogram('email_processing_seconds', 'Time spent processing emails')
LLM_LATENCY = Histogram('llm_response_seconds', 'LLM generation latency')
QUEUE_SIZE = Gauge('email_queue_size', 'Current size of the email queue')

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

def check_redis():
    try:
        r = redis.from_url(REDIS_URL)
        return r.ping()
    except Exception:
        return False

def check_ollama():
    try:
        resp = requests.get(f"{OLLAMA_HOST}")
        return resp.status_code == 200
    except Exception:
        return False

@app.route('/health')
def health():
    redis_status = check_redis()
    ollama_status = check_ollama()
    
    status = 'healthy' if redis_status and ollama_status else 'unhealthy'
    
    return jsonify({
        'status': status,
        'redis': 'up' if redis_status else 'down',
        'ollama': 'up' if ollama_status else 'down'
    }), 200 if status == 'healthy' else 503

@app.route('/')
def index():
    return "AI Email Support API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

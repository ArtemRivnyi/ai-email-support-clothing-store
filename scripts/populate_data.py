import redis
import json
import os
import uuid
import random
import time
from datetime import datetime, timedelta

# Connect to Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
r = redis.from_url(redis_url)

def populate_dashboard():
    print("🚀 Populating Dashboard with Demo Data...")
    
    # 1. Reset current stats (optional, but cleaner for demo)
    # r.flushdb() # Uncomment if you want a clean slate
    
    # 2. Simulate Hourly Traffic (Last 24h)
    print("📊 Generating Hourly Traffic...")
    traffic_pattern = [5, 2, 1, 0, 0, 1, 3, 8, 15, 25, 40, 35, 30, 28, 32, 38, 45, 40, 25, 15, 10, 8, 5, 3]
    for hour, count in enumerate(traffic_pattern):
        r.set(f'emails:hour:{hour}:count', count)
    
    # 3. Simulate Total Counts
    total_emails = sum(traffic_pattern)
    success_count = int(total_emails * 0.85)
    failed_count = int(total_emails * 0.05)
    ignored_count = total_emails - success_count - failed_count
    
    r.set('emails:today:count', total_emails)
    r.set('emails:status:Success:count', success_count)
    r.set('emails:status:Failed:count', failed_count)
    r.set('emails:status:Ignored:count', ignored_count)
    
    # 4. Simulate Response Time
    avg_time = 2.3
    r.set('emails:response_time:count', success_count)
    r.set('emails:response_time:sum', success_count * avg_time)
    
    # 5. Simulate Recent Activity
    print("📝 Generating Recent Activity...")
    senders = ["alice@example.com", "bob@gmail.com", "charlie@yahoo.com", "dave@hotmail.com", "eve@corp.com"]
    subjects = ["Order Status", "Return Request", "Shipping Delay", "Wrong Size", "Spam Offer", "Partnership"]
    statuses = ["Replied", "Replied", "Replied", "Failed", "Ignored", "Replied"]
    
    # Clear old recent list
    r.delete('emails:recent')
    
    for i in range(10):
        entry = {
            'Time': (datetime.now() - timedelta(minutes=i*5)).strftime('%H:%M'),
            'Sender': random.choice(senders),
            'Subject': random.choice(subjects),
            'Status': random.choice(statuses),
            'ID': str(uuid.uuid4())[:8]
        }
        r.rpush('emails:recent', json.dumps(entry))
        
    print("✅ Dashboard Populated! Check http://localhost:8501")

if __name__ == "__main__":
    populate_dashboard()

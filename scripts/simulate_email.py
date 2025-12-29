import redis
import json
import os
import uuid
from datetime import datetime

# Connect to Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
r = redis.from_url(redis_url)

class MockEmail:
    def __init__(self, id, sender, subject, text):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.text = text
        self.thread_id = id # simple mock

def simulate_email(sender, subject, body):
    email_id = str(uuid.uuid4())
    
    # Create a mock email object structure that the worker expects
    # The worker expects an object with .id, .sender, .subject, .text, .thread_id
    
    email_obj = MockEmail(email_id, sender, subject, body)
    
    # Enqueue directly to 'emails' queue
    # Note: RQ typically pickles the job. 
    # To keep it simple and compatible with our worker which uses RQ:
    from rq import Queue
    q = Queue('emails', connection=r)
    
    # We need to enqueue the function call
    q.enqueue('services.email_processor.EmailProcessor().process_email', email_obj)
    
    print(f"✅ Simulated email sent!")
    print(f"From: {sender}")
    print(f"Subject: {subject}")
    print(f"ID: {email_id}")
    print("Check the Dashboard to see it process!")

if __name__ == "__main__":
    print("--- Email Simulator ---")
    print("1. Send 'Where is my order?' (Should be replied)")
    print("2. Send 'Spam offer' (Should be ignored)")
    choice = input("Choose (1/2): ")
    
    if choice == '1':
        simulate_email("customer@example.com", "Order Status", "Hi, where is my order #12345?")
    else:
        simulate_email("spammer@bad.com", "Cheap Rolex", "Buy cheap watches now!")

import os
import time
from redis import Redis
from rq import Worker, Queue, Connection
from services.email_processor import EmailProcessor
from services.gmail_service import get_new_emails, get_gmail_service
from utils.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_MINUTES', 5)) * 60

def fetch_and_queue_emails():
    """
    Periodic task to fetch emails from Gmail and push them to Redis Queue.
    In a real production setup, this might be a separate 'beat' scheduler or cron job.
    For simplicity here, the worker can run this in a separate thread or we just have a loop.
    Actually, let's make this a standalone loop that runs in the 'worker' container 
    if we treat 'worker' as the email fetcher + processor, OR we separate them.
    
    For this plan, let's assume this script runs the RQ Worker, 
    but we also need something to PUT jobs into the queue.
    
    Let's add a simple loop here that fetches emails and enqueues them if the queue is empty,
    or use a separate script. 
    
    Better approach for Week 1: 
    The 'worker' service runs the RQ worker.
    We need a 'beat' or 'producer' service. 
    For now, let's include a producer loop in this file that runs if a specific flag is set,
    OR just have a simple loop that fetches and processes immediately if we weren't using RQ strictly yet.
    
    But the plan says "Worker ... processes queue async".
    So we need a producer.
    Let's create a `producer.py` or just add a function here that we can run.
    
    Let's make `worker.py` purely the RQ worker.
    And we need a `scheduler.py` or `producer.py` to fetch emails.
    
    Wait, the `docker-compose` only has `worker`.
    Let's make `worker.py` start the RQ worker, but we also need to fetch emails.
    
    Let's modify `worker.py` to start a background thread that fetches emails and enqueues them,
    while the main thread runs the RQ worker.
    """
    
    redis_conn = Redis.from_url(REDIS_URL)
    q = Queue('emails', connection=redis_conn)
    gmail_service = get_gmail_service()
    
    logger.info("starting_email_fetcher_loop")
    while True:
        try:
            logger.info("checking_new_emails")
            emails = get_new_emails(gmail_service, query='is:unread')
            for email in emails:
                # Enqueue the email object (or ID)
                # Note: Pickling complex objects like EmailMessage is fine with RQ
                q.enqueue('services.email_processor.EmailProcessor().process_email', email)
                logger.info("enqueued_email", email_id=email.id)
        except Exception as e:
            logger.error("fetcher_error", error=str(e))
        
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    # Start the fetcher in a background thread (simple solution for now)
    import threading
    fetcher_thread = threading.Thread(target=fetch_and_queue_emails, daemon=True)
    fetcher_thread.start()

    # Start RQ Worker
    redis_conn = Redis.from_url(REDIS_URL)
    with Connection(redis_conn):
        worker = Worker(['emails'])
        worker.work()

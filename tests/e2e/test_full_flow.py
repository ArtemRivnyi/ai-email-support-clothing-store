"""
End-to-end test: Send test email -> Process -> Verify reply
"""
import pytest
import time
from services.gmail_service import GmailService
from services.email_processor import queue_email, get_queue_stats

@pytest.mark.e2e
def test_full_email_flow():
    """Test complete email processing flow"""
    gmail = GmailService()
    
    # Step 1: Send test email to yourself
    test_subject = f"Test Order Status - {int(time.time())}"
    test_body = "What is the status of my order #12345?"
    
    print("📧 Sending test email...")
    gmail.send_email(
        to="YOUR_EMAIL@gmail.com",  # Change this
        subject=test_subject,
        body=test_body
    )
    
    # Step 2: Wait for email to arrive
    print("⏳ Waiting for email...")
    time.sleep(5)
    
    # Step 3: Fetch and queue email
    emails = gmail.fetch_unread_emails(query=f"subject:{test_subject}")
    assert len(emails) > 0, "Test email not found"
    
    email_data = emails[0]
    job_id = queue_email(email_data)
    print(f"✅ Email queued: {job_id}")
    
    # Step 4: Wait for processing
    print("⏳ Waiting for worker to process...")
    time.sleep(10)
    
    # Step 5: Verify response was sent
    replies = gmail.fetch_emails(query=f"subject:Re: {test_subject}")
    assert len(replies) > 0, "Reply not found"
    
    print("✅ Full flow test passed!")
    print(f"📨 Reply body preview: {replies[0]['body'][:100]}...")

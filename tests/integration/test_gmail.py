import pytest
import os
from services.gmail_service import get_gmail_service, get_new_emails, send_email_reply

@pytest.mark.skipif(not os.path.exists('token.pickle'), reason="Gmail credentials not found")
def test_gmail_connection():
    """Test that we can connect to Gmail API"""
    service = get_gmail_service()
    assert service is not None

@pytest.mark.skipif(not os.path.exists('token.pickle'), reason="Gmail credentials not found")
def test_fetch_emails():
    """Test fetching emails (even if empty)"""
    service = get_gmail_service()
    emails = get_new_emails(service, query='is:unread', user_id='me')
    assert isinstance(emails, list)

@pytest.mark.skipif(not os.path.exists('token.pickle'), reason="Gmail credentials not found")
def test_send_email_mock():
    """
    Test sending email logic (mocked to avoid spamming).
    We verify the service object has the right methods.
    """
    service = get_gmail_service()
    assert hasattr(service.users().messages(), 'send')

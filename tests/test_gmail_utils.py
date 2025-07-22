import pytest
from gmail_utils import EmailMessage, send_email_reply, mark_email_as_read

class DummyService:
    def __init__(self):
        self.users_calls = []

    def users(self):
        return self

    def messages(self):
        return self

    def send(self, userId, body):
        self.users_calls.append(("send", userId, body))
        return DummyExecute({"id": "123456"})

    def modify(self, userId, id, body):
        self.users_calls.append(("modify", userId, id, body))
        return DummyExecute({"id": id})

class DummyExecute:
    def __init__(self, result):
        self.result = result
    def execute(self):
        return self.result

def test_send_email_reply():
    service = DummyService()
    result = send_email_reply(
        service=service,
        original_message_id="original123",
        to="user@example.com",
        subject="Тестовая тема",
        message_text="Привет!",
        thread_id="thread456"
    )
    assert result is not None
    assert result['id'] == "123456"

def test_mark_email_as_read():
    service = DummyService()
    mark_email_as_read(service=service, message_id="email789")
    calls = service.users_calls
    assert calls[0][0] == "modify"
    assert calls[0][2]["removeLabelIds"] == ["UNREAD"]

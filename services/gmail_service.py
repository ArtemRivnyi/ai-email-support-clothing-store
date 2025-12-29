# gmail_service.py
import os
import pickle
import json
import base64
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from dotenv import load_dotenv
from auth.oauth_manager import OAuthManager

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']
TOKEN_FILE = 'token.pickle'
CREDS_FILE = 'credentials.json'

class EmailMessage:
    def __init__(self, id, sender, recipient, subject, text, thread_id):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.text = text
        self.thread_id = thread_id

def get_gmail_service():
    """
    Initializes Gmail API service using OAuthManager.
    """
    creds = OAuthManager.get_credentials()
    if not creds:
        return None

    return build('gmail', 'v1', credentials=creds)

def get_new_emails(service, user_id='me', query='is:unread'):
    """
    Fetches unread emails.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get('messages', [])
        email_list = []

        if not messages:
            logging.info('No unread messages found.')
        else:
            for message_item in messages:
                msg = service.users().messages().get(userId=user_id, id=message_item['id'], format='full').execute()
                payload = msg['payload']
                headers = payload['headers']

                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                recipient = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown Recipient')
                thread_id = msg['threadId']

                msg_text = ""
                def get_text_part(parts):
                    for part in parts:
                        if part['mimeType'] == 'text/plain' and 'body' in part and 'data' in part['body']:
                            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        elif 'parts' in part:
                            recursive_text = get_text_part(part['parts'])
                            if recursive_text:
                                return recursive_text
                    return None

                if 'parts' in payload:
                    msg_text = get_text_part(payload['parts'])
                elif 'body' in payload and 'data' in payload['body']:
                    msg_text = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
                
                if not msg_text:
                    msg_text = "[Text not found]"

                email_list.append(EmailMessage(message_item['id'], sender, recipient, subject, msg_text, thread_id))
        return email_list
    except Exception as e:
        logging.error(f'Error fetching emails: {e}')
        return []

def send_email_reply(service, original_message_id: str, to: str, subject: str, message_text: str, thread_id: str):
    """
    Sends a reply.
    """
    try:
        message = MIMEText(message_text, 'plain', 'utf-8')
        message['to'] = to
        message['subject'] = f"Re: {subject}"
        message['In-Reply-To'] = original_message_id
        message['References'] = original_message_id

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message, 'threadId': thread_id}

        message_sent = service.users().messages().send(userId='me', body=body).execute()
        logging.info(f'Reply sent to {to} for message ID {original_message_id}.')
        return message_sent
    except Exception as e:
        logging.error(f'Error sending email: {e}')
        return None

def mark_email_as_read(service, message_id: str, user_id='me'):
    """
    Marks email as read.
    """
    try:
        service.users().messages().modify(userId=user_id, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        logging.info(f"Email {message_id} marked as read.")
    except Exception as e:
        logging.error(f"Error marking email {message_id} as read: {e}")
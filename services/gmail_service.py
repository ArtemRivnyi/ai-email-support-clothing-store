# gmail_utils.py
import os
import pickle
import json
import base64
import logging # Добавляем для логирования
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv() # Загружаем переменные окружения

# Настройка логирования для этого модуля
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Если вы измените SCOPES, вам нужно будет удалить файл token.pickle
# и снова пройти аутентификацию.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']
TOKEN_FILE = 'token.pickle' # Файл для хранения токенов доступа и обновления пользователя
CREDS_FILE = 'credentials.json' # Временный файл для хранения client_id/secret для flow

class EmailMessage:
    def __init__(self, id, sender, recipient, subject, text, thread_id):
        self.id = id
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get('messages', [])
        email_list = []

        if not messages:
            logging.info('Непрочитанных сообщений не найдено.')
        else:
            for message_item in messages:
                msg = service.users().messages().get(userId=user_id, id=message_item['id'], format='full').execute()
                payload = msg['payload']
                headers = payload['headers']

                # Извлекаем отправителя, тему и получателя
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Неизвестный отправитель')
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Без темы')
                recipient = next((h['value'] for h in headers if h['name'] == 'To'), 'Неизвестный получатель')
                thread_id = msg['threadId']

                # Получаем текстовое тело письма
                msg_text = ""
                # Рекурсивная функция для поиска текстовой части
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
                    msg_text = "[Текст письма не найден или не может быть декодирован]" # Заглушка, если текст не найден

                email_list.append(EmailMessage(message_item['id'], sender, recipient, subject, msg_text, thread_id))
        return email_list
    except Exception as e:
        logging.error(f'Произошла ошибка при получении писем: {e}')
        return []

def send_email_reply(service, original_message_id: str, to: str, subject: str, message_text: str, thread_id: str):
    """
    Отправляет ответ на электронное письмо, сохраняя его в той же цепочке.
    """
    try:
        message = MIMEText(message_text, 'plain', 'utf-8') # Указываем кодировку UTF-8
        message['to'] = to
        message['subject'] = f"Re: {subject}" # Префикс для ответов
        message['In-Reply-To'] = original_message_id
        message['References'] = original_message_id # Помогает группировать сообщения

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message, 'threadId': thread_id} # Важно для цепочки сообщений

        message_sent = service.users().messages().send(userId='me', body=body).execute()
        logging.info(f'Ответ отправлен на {to} для сообщения ID {original_message_id} в цепочке {thread_id}. ID сообщения: {message_sent["id"]}')
        return message_sent
    except Exception as e:
        logging.error(f'Произошла ошибка при отправке письма: {e}')
        return None

def mark_email_as_read(service, message_id: str, user_id='me'):
    """
    Помечает письмо как прочитанное.
    """
    try:
        # Убедимся, что removeLabelIds - это список, даже если один элемент
        service.users().messages().modify(userId=user_id, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        logging.info(f"Письмо {message_id} помечено как прочитанное.")
    except Exception as e:
        logging.error(f"Ошибка при пометке письма {message_id} как прочитанного: {e}")
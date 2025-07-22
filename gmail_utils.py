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
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.text = text
        self.thread_id = thread_id # Важно для ответа в той же цепочке

def get_gmail_service():
    """
    Инициализирует сервис Gmail API. Читает token.pickle для аутентифицированного пользователя
    или запрашивает авторизацию.
    """
    creds = None
    # Файл token.pickle хранит токены доступа и обновления пользователя
    # и создается автоматически при первом завершении потока авторизации.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Если нет (действительных) доступных учетных данных, дайте пользователю войти.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logging.info("Токен истек, обновляем...")
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Ошибка при обновлении токена: {e}. Возможно, потребуется повторная авторизация.")
                creds = None # Сброс, чтобы запросить новую авторизацию
        else:
            logging.info("Требуется новая авторизация Gmail API...")
            # Нам нужно создать credentials.json на лету из переменных .env
            client_id = os.getenv("GOOGLE_CLIENT_ID")
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

            if not client_id or not client_secret:
                logging.error("Ошибка: GOOGLE_CLIENT_ID или GOOGLE_CLIENT_SECRET не найдены в .env. Пожалуйста, проверьте ваш .env файл.")
                return None

            # Создаем временную структуру credentials.json для google-auth-oauthlib
            creds_data = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "project_id": "ai-email-support-project", # Заглушка
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"] # Требуется для Desktop app
                }
            }
            
            # Сохраняем временный файл credentials.json
            try:
                with open(CREDS_FILE, 'w') as f:
                    json.dump(creds_data, f)
            except Exception as e:
                logging.error(f"Ошибка при создании временного файла {CREDS_FILE}: {e}")
                return None
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
                creds = flow.run_local_server(port=0) # Открывает браузер для аутентификации
            except Exception as e:
                logging.error(f"Ошибка при прохождении OAuth потока: {e}. Убедитесь, что ваш Client ID/Secret корректны и приложение настроено как 'Desktop app' в Google Cloud Console. Также проверьте, что аккаунт добавлен в 'Test users'.")
                return None
            finally:
                # Удаляем временный файл credentials.json
                if os.path.exists(CREDS_FILE):
                    os.remove(CREDS_FILE)

    # Сохраняем учетные данные для следующего запуска
    if creds and creds.valid:
        try:
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            logging.error(f"Ошибка при сохранении токена в {TOKEN_FILE}: {e}")
            return None
    else:
        return None # Если после попытки авторизации нет действительных creds

    return build('gmail', 'v1', credentials=creds)

def get_new_emails(service, user_id='me', query='is:unread'):
    """
    Извлекает непрочитанные письма из почтового ящика пользователя.
    """
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
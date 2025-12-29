import os
import pickle
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config.secrets import secrets
from utils.logger import get_logger

logger = get_logger(__name__)

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.modify']
TOKEN_FILE = 'token.pickle'
CREDS_FILE = 'credentials.json'

class OAuthManager:
    @staticmethod
    def get_credentials():
        """
        Gets valid user credentials from storage.
        Refreshes them if expired.
        """
        creds = None
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, 'rb') as token:
                    creds = pickle.load(token) # nosec B301
            except Exception as e:
                logger.error("failed_to_load_token", error=str(e))

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("token_expired_refreshing")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error("token_refresh_failed", error=str(e))
                    creds = None
            
            if not creds:
                logger.info("initiating_new_auth_flow")
                creds = OAuthManager._run_auth_flow()

            if creds:
                OAuthManager._save_credentials(creds)

        return creds

    @staticmethod
    def _run_auth_flow():
        client_id = secrets.get_secret("GOOGLE_CLIENT_ID")
        client_secret = secrets.get_secret("GOOGLE_CLIENT_SECRET")

        if not client_id or not client_secret:
            logger.error("missing_client_secrets")
            return None

        # Create temporary credentials.json
        creds_data = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "project_id": "ai-email-support",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
            }
        }
        
        try:
            with open(CREDS_FILE, 'w') as f:
                json.dump(creds_data, f)
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            return creds
        except Exception as e:
            logger.error("auth_flow_failed", error=str(e))
            return None
        finally:
            if os.path.exists(CREDS_FILE):
                os.remove(CREDS_FILE)

    @staticmethod
    def _save_credentials(creds):
        try:
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            logger.info("credentials_saved")
        except Exception as e:
            logger.error("failed_to_save_credentials", error=str(e))

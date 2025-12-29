"""
Generate Gmail OAuth token for the AI Email Support System
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def generate_token():
    """Generate Gmail API token"""
    creds = None
    
    # Check if token already exists
    if os.path.exists('token.pickle'):
        print("Loading existing token...")
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)  # nosec B301
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token...")
            creds.refresh(Request())
        else:
            print("Generating new token...")
            print("\n🔐 This will open your browser for authentication")
            print("Please allow all requested permissions\n")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        # Save token
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        
        print("\n✅ Token generated successfully!")
        print("📁 Saved as token.pickle")
    else:
        print("✅ Token is valid!")
    
    return creds

if __name__ == '__main__':
    print("🚀 Gmail Token Generator for AI Email Support\n")
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ Error: credentials.json not found!")
        print("📝 Please download it from Google Cloud Console")
        print("📖 See docs/GMAIL_SETUP.md for instructions")
        exit(1)
    
    generate_token()

#!/usr/bin/env python3
"""
Gmail OAuth Token Generator for AI Email Support System

This script generates OAuth tokens for Gmail API access.
It will open a browser window for authentication.

Usage:
    python scripts/generate_token.py
"""

import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

# File paths
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def check_credentials():
    """Check if credentials.json exists"""
    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ Error: credentials.json not found!")
        print("\n📝 Please follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project and enable Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download credentials.json")
        print("\n📖 Detailed guide: docs/GMAIL_SETUP.md")
        sys.exit(1)

def generate_token():
    """Generate OAuth token"""
    creds = None
    
    # Check for existing token
    if os.path.exists(TOKEN_FILE):
        print("🔍 Found existing token, checking validity...")
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)  # nosec B301
    
    # Validate or generate new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
            except Exception as e:
                print(f"❌ Failed to refresh token: {e}")
                print("🔄 Generating new token...")
                creds = None
        
        if not creds:
            print("\n🌐 Opening browser for authentication...")
            print("👤 Please login with your Gmail account")
            print("✅ Click 'Allow' to grant permissions\n")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    success_message='✅ Authentication successful! You can close this window.'
                )
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                sys.exit(1)
        
        # Save token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print(f"\n✅ Token saved as {TOKEN_FILE}")
    else:
        print("✅ Token is valid!")
    
    return creds

def verify_token(creds):
    """Verify token by making a test API call"""
    try:
        from googleapiclient.discovery import build
        
        print("\n🔬 Testing Gmail API connection...")
        service = build('gmail', 'v1', credentials=creds)
        
        # Test call - get user profile
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress')
        
        print(f"✅ Successfully connected to Gmail!")
        print(f"📧 Authenticated as: {email}")
        print(f"📊 Total messages: {profile.get('messagesTotal', 0)}")
        
        return True
    except Exception as e:
        print(f"❌ Gmail API test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 Gmail Token Generator for AI Email Support")
    print("=" * 60)
    print()
    
    # Check for credentials
    check_credentials()
    
    # Generate token
    creds = generate_token()
    
    # Verify
    if verify_token(creds):
        print("\n" + "=" * 60)
        print("🎉 Setup Complete!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("1. Update .env file with paths")
        print("2. Run: docker-compose up -d")
        print("3. Check logs: docker-compose logs -f worker")
        print("\n📖 See README.md for more information")
    else:
        print("\n⚠️  Token generated but verification failed")
        print("Please check your Gmail API configuration")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)



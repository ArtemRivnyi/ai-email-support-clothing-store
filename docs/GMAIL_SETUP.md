# Gmail API Setup Guide

## Prerequisites
- Google Cloud Project
- Gmail account for the bot

## Steps

### 1. Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Click "Create Project"
3. Name: "AI Email Support"
4. Click "Create"

### 2. Enable Gmail API
1. Go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 3. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "AI Email Bot"
5. Download credentials.json

### 4. Configure OAuth Consent Screen
1. Go to "OAuth consent screen"
2. User Type: "External"
3. Add scopes:
   - .../auth/gmail.readonly
   - .../auth/gmail.send
   - .../auth/gmail.modify
4. Add your email as test user

### 5. Generate Token
```bash
python scripts/generate_token.py
# This will open browser and save token.json
```

### 6. Update .env
```env
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_TOKEN_PATH=./token.json
```

## Troubleshooting

**Error: "Access blocked: This app's request is invalid"**
- Solution: Add your email to test users in OAuth consent screen

**Error: "insufficient authentication scopes"**
- Solution: Delete token.json and re-authenticate

# 🔐 Gmail API Setup Guide

Complete guide to configure Gmail API for AI Email Support System.

## Prerequisites
- Google account
- 10 minutes

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"**
3. Project name: `ai-email-support`
4. Click **"Create"**

---

## Step 2: Enable Gmail API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search: `Gmail API`
3. Click **"Enable"**

---

## Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen first:
   - User Type: **External**
   - App name: `AI Email Support`
   - User support email: your email
   - Developer contact: your email
   - Click **"Save and Continue"**
   - Scopes: click **"Add or Remove Scopes"**
     - Search and add: `gmail.readonly`, `gmail.send`, `gmail.modify`
   - Test users: Add your Gmail address
   - Click **"Save and Continue"**

4. Back to Create OAuth client ID:
   - Application type: **"Desktop app"**
   - Name: `AI Email Bot`
   - Click **"Create"**

5. **Download JSON**:
   - Click the download button (⬇️) next to your OAuth client
   - Save as `credentials.json` in project root

---

## Step 4: Generate Access Token

Run the token generator script:
```bash
python scripts/generate_token.py
```

This will:
1. Open your browser
2. Ask you to login with Google
3. Request permissions (click "Allow")
4. Generate `token.pickle` file

---

## Step 5: Verify Setup
```bash
# Test Gmail connection
python -c "
from services.gmail_service import GmailService
gmail = GmailService()
print('✅ Gmail API connected!')
"
```

---

## 🔒 Security Notes

- `credentials.json` contains your OAuth client secrets
- `token.pickle` contains access tokens
- **Never commit these files to Git** (already in .gitignore)
- Tokens auto-refresh every 7 days

---

## ❌ Troubleshooting

### Error: "Access blocked: This app's request is invalid"
**Solution:** Add your email to test users in OAuth consent screen

### Error: "insufficient authentication scopes"
**Solution:** Delete `token.pickle` and re-run `generate_token.py`

### Error: "Token has been expired or revoked"
**Solution:** Run `python scripts/generate_token.py` to refresh

---

## 🎯 Next Steps

After setup:
1. Update `.env` with paths
2. Start the system: `docker-compose up -d`
3. Check logs: `docker-compose logs -f worker`



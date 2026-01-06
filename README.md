<p align="left">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/Gmail%20API-Enabled-red.svg" alt="Gmail API Enabled" />
  <img src="https://img.shields.io/badge/OAuth-2.0-green.svg" alt="OAuth 2.0" />
  <img src="https://img.shields.io/badge/License-MIT-black.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg" alt="Stable" />
</p>

# ⭐ Seventy-Seven Thousand Unread Emails - Mark All Unread Emails as Read in Gmail ✉️

At some point, I stopped reading my emails and simply… never recovered. One unread message became many, many became thousands, and eventually Gmail was showing 77,000 unread emails.

Since Gmail does not offer a practical way to mark that many messages as read, this script exists to clean up the mess—quickly and safely.

This repository contains a Python script that connects to your Gmail account using the **Gmail API** and **OAuth 2.0**, retrieves all unread emails, and marks them as read in efficient batches.

It is designed to safely handle very large inboxes (tens of thousands of unread messages) while respecting Gmail API rate limits.


## 🚀 What This Script Does

- Authenticates securely using Google OAuth 2.0
- Searches for unread Gmail messages (`is:unread`)
- Processes messages in batches of up to 1,000 (Gmail API limit)
- Marks all matched messages as **read**
- Automatically retries transient API errors (429 / 500 / 503)

## 🛠 Requirements

- Python 3.9+
- A Google account
- Gmail enabled on the account

### Python Dependencies
Install required packages:

```bash
pip install --upgrade google-api-python-client google-auth google-auth-oauthlib
```


## 🔐 Gmail API Setup (Step-by-Step)

In order to use you first need to enable the Gmail API on your account.

### 1. Create a Project
- Go to the **Google Cloud Console**
- Create a **new project**

### 2. Enable the Gmail API
- Navigate to **APIs & Services → Library**
- Search for **Gmail API**
- Click **Enable**

### 3. Configure OAuth Consent Screen
- Go to **APIs & Services → OAuth consent screen**
- Select **External** (unless using Google Workspace)
- Click **Create**
- Fill in:
  - **App Name**
  - **Support Email**
- You can skip optional fields for now
- **Important:** Under **Test Users**, add **your own email address** so you can authenticate immediately

### 4. Create OAuth Credentials
- Go to **APIs & Services → Credentials**
- Click **Create Credentials → OAuth client ID**
- Application type: **Desktop app**
- Download the JSON file
- Rename it to:

```text
credentials.json
```

- Place it in the same folder as the Python script


## ▶️ How to Run

```bash
python mark_unread_as_read.py
```

On first run:
- A browser window will open
- You will be asked to sign in to Google
- You must approve Gmail access

After approval:
- A local file named `token.json` is created
- Future runs will reuse this token automatically


## 🔍 Search Behavior

By default, the script searches:
```text
is:unread
```

This includes unread messages in normal Gmail locations (Inbox, labels, etc.).

If you want **everything**, including Spam and Trash, you can change:
```python
query = "is:unread in:anywhere"
```


## 🔐 Permissions Used

The script uses the following OAuth scope:

```text
https://www.googleapis.com/auth/gmail.modify
```

This allows the script to:
- Read message metadata
- Modify labels (required to remove `UNREAD`)

It does **not** delete messages or access other Google services.


## 🧠 Notes on Large Inboxes

- Gmail API limits batch operations to 1,000 messages
- This script automatically chunks requests
- Built-in exponential backoff prevents rate-limit failures
- Designed to safely handle 50,000+ unread messages

## 🚧 Future Upgrades

I plan on adding a user interface and the ability to download emails and delete those emails that have already been downloaded. 

That is on-going and will update once I have it completed.

## ⚖️ Use at Your Own Risk Disclaimer

This software is provided **"as is"**, without warranty of any kind, express or implied.

By using this script, you acknowledge and agree that:

- You are solely responsible for how the script is used
- You are responsible for securing your Google account, OAuth credentials, and tokens
- You are responsible for complying with Google’s Terms of Service and applicable laws
- The author assumes **no responsibility or liability** for:
  - Data loss
  - Account compromise
  - Security breaches
  - API misuse
  - Any direct or indirect damages resulting from use of this script

Use this tool **only** on accounts you own or have explicit authorization to access.


## 📜 Disclaimer

This project is intended for educational and personal automation purposes only.
## 📌 License

MIT License

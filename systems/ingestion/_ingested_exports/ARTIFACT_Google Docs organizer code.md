---
title: Google Docs organizer code
domain: 06_AGENT_LAYER
source: chatgpt: 2025-11-14_Google_Docs_organizer_code.md
tags: chatgpt, council-grove, distilled-candidate,full-body
type: knowledge_artifact
---

# Google Docs organizer code
**Domain:** 06_AGENT_LAYER
**Source:** chatgpt: 2025-11-14_Google_Docs_organizer_code.md

# Google Docs organizer code
> **Source:** ChatGPT  |  **Date:** 2025-11-14  |  **Stage:** `DISTILLED_CANDIDATE`  |  **Pillar:** `06_AGENTS`

---

## Transcript

### ∆ **USER** — 2025-11-14 23:09

Create the code for Google ai studio to make an app to organize my Google docs and get rid of anything redundant.

---

### ⚙ **ASSISTANT** — 2025-11-14 23:09

Nice. Let’s build you a little “Doc Spirit Cleaner” that plugs into Google AI Studio + your Google Drive.

Below is **one clean Python script** that:

- Connects to your Google Drive & Docs  
- Pulls text from your Google Docs  
- Uses **Gemini embeddings** (via Google AI Studio / `google-generativeai`) to find near-duplicate docs  
- Moves “redundant” docs into a **`Duplicates_Review`** folder instead of deleting them (so you don’t accidentally nuke something sacred)

You can later wrap this in a tiny web API and let your AI Studio app call it as a tool.

---

## 1. What you need set up first

1. **Google AI Studio / Gemini API key**
   - In AI Studio, create an API key.
   - On your machine, set:
     ```bash
     export GEMINI_API_KEY="YOUR_API_KEY_HERE"
     ```

2. **Google Cloud project + OAuth credentials for Drive & Docs**
   - In Google Cloud Console, create OAuth 2.0 credentials.
   - Download `client_secret.json` into the same folder as this script.
   - First run will open a browser window to let you log in and approve scopes.

3. Install dependencies:
   ```bash
   pip install google-generativeai google-auth google-auth-oauthlib google-api-python-client python-dotenv
   ```

---

## 2. The script: `doc_deduper.py`

```python
import os
import math
from typing import List, Dict, Tuple

import google.generativeai as genai

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ===================== CONFIG =====================

# Max number of Docs to scan in one run (to avoid blowing up your quota)
MAX_DOCS = 200

# Embedding model from Google AI Studio
EMBEDDING_MODEL = "text-embedding-004"

# Similarity threshold for "these are basically copies"
DUPLICATE_THRESHOLD = 0.90

# Name of the folder to move duplicates into
DUPLICATES_FOLDER_NAME = "Duplicates_Review"

# Path to your OAuth client secret file (from Google Cloud Console)
CLIENT_SECRET_FILE = "client_secret.json"

# Path where user credentials will be stored after first login
TOKEN_FILE = "token.json"

# Scopes: read/write Drive and read Docs
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents.readonly",
]

# Gemini API key from Google AI Studio
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ===================== AUTH HELPERS =====================

def get_credentials() -> Credentials:
    """Get OAuth credentials for Google APIs (Drive + Docs)."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds


def get_drive_service(creds: Credentials):
    return build("drive", "v3", credentials=creds)


def get_docs_service(creds: Credentials):
    return build("docs", "v1", credentials=creds)

# ===================== GEMINI SETUP =====================

def init_gemini():
    if not GEMINI_API_KEY:
        raise ValueError(
            "Missing GEMINI_API_KEY. Set it as an environment variable."
        )
    genai.configure(api_key=GEMINI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for a list of texts using Gemini embeddings.
    """
    init_gemini()
    response = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=texts,
        task_type="retrieval_document",
    )
    # Response may be a dict with 'embeddings' list
    embeddings = [e["values"] for e in response["embeddings"]]
    return embeddings

# ===================== DRIVE/DOCS HELPERS =====================

def list_google_docs(drive_service, max_docs: int) -> List[Dict]:
    """
    List Google Docs in your Drive (not including non-Docs files).
    """
    docs = []
    page_token = None

    query = "mimeType='application/vnd.google-apps.document' and trashed=false"

    while True:
        response = drive_service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, createdTime, modifiedTime)",
            pageToken=page_token,
            pageSize=min(max_docs - len(docs), 100),
        ).execute()

        files = response.get("files", [])
        docs.extend(files)

 

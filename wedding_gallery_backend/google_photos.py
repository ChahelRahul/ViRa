import os
import json
import logging
import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load environment variables and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Path to your token file
TOKEN_FILE = "token.json"

# ---------------------- Auth Functions ----------------------

def get_flow():
    """Create the OAuth2 flow using the client secret and redirect URI."""
    return Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[os.getenv("SCOPES")],
        redirect_uri=os.getenv("REDIRECT_URI")
    )

def save_token(creds):
    """Save OAuth credentials to token.json."""
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            token_data = json.load(token_file)
            creds = Credentials.from_authorized_user_info(token_data)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            return creds
    else:
        raise Exception("Token file not found")
# ---------------------- Google Photos API ----------------------

def list_albums():
    """List available albums (up to 50)."""
    creds = load_token()
    if not creds:
        return {"error": "Not authenticated"}

    headers = {"Authorization": f"Bearer {creds.token}"}
    res = requests.get('https://photoslibrary.googleapis.com/v1/albums?pageSize=50', headers=headers)
    return res.json()

def get_photos():
    creds = load_token()
    if not creds or not creds.token:
        return {"error": "Not authenticated"}

    album_id = os.getenv("ALBUM_ID")
    if not album_id:
        return {"error": "Missing album ID"}

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    url = "https://photoslibrary.googleapis.com/v1/mediaItems:search"
    payload = {"albumId": album_id, "pageSize": 100}

    all_items = []
    while True:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return {"error": response.text}
        
        data = response.json()
        items = data.get("mediaItems", [])
        all_items.extend(items)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
        payload["pageToken"] = next_page_token

    return [
        {
            "url": item["baseUrl"] + "=w2000",
            "filename": item.get("filename", "Photo")
        }
        for item in all_items
    ]

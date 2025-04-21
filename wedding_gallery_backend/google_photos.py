import os
import json
import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()

TOKEN_FILE = "token.json"

def get_flow():
    return Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[os.getenv("SCOPES")],
        redirect_uri=os.getenv("REDIRECT_URI")
    )

def save_token(creds):
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            return json.load(token)

def list_albums():
    token = load_token()
    if not token:
        return {"error": "Not authenticated"}

    headers = {"Authorization": f"Bearer {token['token']}"}
    res = requests.get('https://photoslibrary.googleapis.com/v1/albums?pageSize=50', headers=headers)
    return res.json()

def get_photos():
    token = load_token()
    if not token:
        return {"error": "Not authenticated"}

    headers = {"Authorization": f"Bearer {token['token']}"}
    album_id = os.getenv("ALBUM_ID")
    if not album_id:
        return {"error": "Missing ALBUM_ID in .env"}

    body = {"albumId": album_id, "pageSize": 100}

    res = requests.post(
        'https://photoslibrary.googleapis.com/v1/mediaItems:search',
        headers=headers,
        json=body
    )

    data = res.json()
    if "mediaItems" not in data:
        return {"error": "No media found"}

    return [{
        "url": item['baseUrl'] + "=w1000",
        "filename": item['filename']
    } for item in data["mediaItems"]]

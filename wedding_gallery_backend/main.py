import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google_photos import get_flow, save_token, get_photos, list_albums

# Allow HTTP (for local dev)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load env vars
load_dotenv()

# Create app
app = FastAPI()

# Add CORS middleware
origins = [
    "https://chahelrahul.github.io",  # GitHub Pages domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def home():
    return {"message": "Wedding Gallery Backend"}

@app.get("/auth")
def auth():
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def auth_callback(request: Request):
    try:
        flow = get_flow()
        flow.fetch_token(authorization_response=str(request.url))
        creds = flow.credentials
        save_token(creds)
        return RedirectResponse("/albums")
    except Exception as e:
        print("❌ OAuth callback failed:", e)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/albums")
def albums():
    return JSONResponse(list_albums())

@app.get("/photos")
def photos():
    return JSONResponse(get_photos())

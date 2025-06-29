# app.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Initialize FastAPI app
app = FastAPI()

# ------------------- Middleware -------------------
# Allow CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Static files -------------------
# Adjust gallery path as needed based on your folder structure
GALLERY_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/images/gallery"))

# Serve photos under /photos/*
app.mount("/photos", StaticFiles(directory=GALLERY_FOLDER), name="photos")

# ------------------- Routes -------------------

@app.get("/")
def read_root():
    return {"message": "Wedding gallery backend running"}

@app.get("/list_photos")
def list_photos():
    """
    List all image files in the gallery folder.
    """
    files = []
    for f in os.listdir(GALLERY_FOLDER):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            files.append({"url": f"/photos/{f}", "filename": f})
    return files

@app.get("/convert_heic")
def convert_heic_to_jpg():
    """
    Convert all HEIC files in the gallery folder to JPG.
    """
    converted = []

    for file in os.listdir(GALLERY_FOLDER):
        if file.lower().endswith(".heic"):
            input_path = os.path.join(GALLERY_FOLDER, file)
            output_path = os.path.join(GALLERY_FOLDER, os.path.splitext(file)[0] + ".jpg")

            try:
                img = Image.open(input_path)
                img.save(output_path, "JPEG")
                converted.append({"input": file, "output": os.path.basename(output_path)})
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to convert {file}: {str(e)}"}
                )

    return {"converted_files": converted, "message": f"Converted {len(converted)} HEIC files to JPG."}

import os
from uuid import uuid4
from fastapi import HTTPException, status
from PIL import Image

UPLOAD_DIR = "static/uploads"

os.makedirs(f"{UPLOAD_DIR}/products", exist_ok=True)
os.makedirs(f"{UPLOAD_DIR}/profiles", exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".png", ".jpeg", ".webp"}

def save_upload(upload_file, folder:str) -> str :

    if not upload_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image is required")
    
    ext = os.path.splitext(upload_file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Only JPG, PNG, and Webp Images are allowed")
    
    file_id = uuid4().hex
    file_name = f"{file_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, folder, file_name)

    try:
        with Image.open(upload_file.file) as img:
            img.thumbnail((1200 ,1200))
            img.save(file_path, optimize=True, quality=85)

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    return f"static/uploads/{folder}/{file_name}"

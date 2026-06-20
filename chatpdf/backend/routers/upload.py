import os
from fastapi import APIRouter, UploadFile, File
from services.rag import build_vectorstore

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    build_vectorstore(filepath)

    return {"message": "PDF processed", "filename": file.filename}
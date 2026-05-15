from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.rag_pipeline import process_pdf, ask_question

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG System Running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = f"{UPLOAD_FOLDER}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_pdf(file_path)

        return {
            "message": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/ask")
def ask(question: str):
    try:
        answer = ask_question(question)

        return {
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }
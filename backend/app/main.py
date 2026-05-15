from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

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

# create uploads folder automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Backend Running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        process_pdf(file_path)

        return {
            "message": "PDF uploaded successfully",
            "filename": file.filename
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/ask")
def ask(query: str):
    try:
        answer = ask_question(query)
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
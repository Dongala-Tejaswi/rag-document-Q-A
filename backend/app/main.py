from fastapi import FastAPI, UploadFile, File
from app.rag_pipeline import process_pdf, ask_question
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "RAG System Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    process_pdf(path)

    return {"message": "PDF uploaded successfully"}

@app.get("/ask")
def ask(query: str):

    answer = ask_question(query)

    return {"answer": answer}
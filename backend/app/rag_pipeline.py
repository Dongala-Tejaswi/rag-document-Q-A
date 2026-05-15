import fitz

from app.embedding import create_embedding
from app.vector_store import (
    store_embeddings,
    search_embeddings
)

stored_chunks = []


def process_pdf(file_path):

    global stored_chunks

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    chunks = text.split("\n")

    chunks = [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip()) > 20
    ]

    stored_chunks = chunks

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)

    return "PDF processed successfully"


def ask_question(question):

    query_embedding = create_embedding([question])[0]

    results = search_embeddings(query_embedding)

    if not results:
        return "No relevant answer found."

    return "\n".join(results)
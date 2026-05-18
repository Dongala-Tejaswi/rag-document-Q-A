import fitz
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

chunks = []
embeddings = None

# Lightweight accurate model
model = SentenceTransformer('all-MiniLM-L6-v2')


def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def create_chunks(text, chunk_size=500):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    smart_chunks = []

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) < chunk_size:

            current_chunk += " " + sentence

        else:

            smart_chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        smart_chunks.append(current_chunk.strip())

    return smart_chunks


def process_pdf(file_path):

    global chunks, embeddings

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:

        text = page.get_text("text")

        full_text += text + "\n"

    full_text = clean_text(full_text)

    if len(full_text) < 20:
        return "No readable text found"

    chunks = create_chunks(full_text)

    chunks = [chunk for chunk in chunks if len(chunk) > 40]

    if len(chunks) == 0:
        return "No valid chunks generated"

    # Generate semantic embeddings
    embeddings = model.encode(chunks)

    return "PDF uploaded successfully"


def ask_question(query):

    global chunks, embeddings

    if embeddings is None:
        return "Please upload PDF first"

    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    top_indices = similarities.argsort()[-3:][::-1]

    results = []

    for idx in top_indices:

        score = similarities[idx]

        if score > 0.25:
            results.append(chunks[idx])

    if len(results) == 0:
        return "Answer not found in document"

    return "\n\n".join(results)
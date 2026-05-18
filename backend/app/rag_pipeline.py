import fitz
import re
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# GLOBAL STORAGE
# -----------------------------

chunks = []
embeddings = None

# Lightweight accurate model
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# CLEAN TEXT
# -----------------------------

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------
# SMART CHUNKING
# -----------------------------

def create_chunks(text, chunk_size=700):

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


# -----------------------------
# PROCESS PDF
# -----------------------------

def process_pdf(file_path):

    global chunks, embeddings

    chunks = []
    embeddings = None

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:

        text = page.get_text("text")

        full_text += text + "\n"

    full_text = clean_text(full_text)

    if len(full_text) < 20:
        return "No readable text found"

    # Create smart chunks
    chunks = create_chunks(full_text)

    chunks = [c for c in chunks if len(c) > 50]

    if len(chunks) == 0:
        return "No valid chunks generated"

    # Generate embeddings
    embeddings = model.encode(chunks)

    return f"PDF uploaded successfully. Total chunks: {len(chunks)}"


# -----------------------------
# ASK QUESTION
# -----------------------------

def ask_question(query):

    global chunks, embeddings

    if embeddings is None or len(chunks) == 0:
        return "Please upload PDF first"

    # Encode question
    query_embedding = model.encode([query])

    # Similarity search
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # Get top 5 chunks
    top_indices = similarities.argsort()[-5:][::-1]

    best_results = []

    query_words = query.lower().split()

    for idx in top_indices:

        chunk = chunks[idx]

        score = similarities[idx]

        # Keyword boosting
        keyword_matches = 0

        for word in query_words:

            if word in chunk.lower():
                keyword_matches += 1

        final_score = score + (keyword_matches * 0.08)

        best_results.append(
            (final_score, chunk)
        )

    # Sort final results
    best_results = sorted(
        best_results,
        reverse=True
    )

    # Return top answers
    final_answers = []

    for score, chunk in best_results[:3]:

        if score > 0.20:
            final_answers.append(chunk)

    if len(final_answers) == 0:
        return "Answer not found in document"

    return "\n\n".join(final_answers)
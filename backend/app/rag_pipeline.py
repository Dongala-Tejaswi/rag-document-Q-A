import fitz
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# GLOBAL STORAGE
# -----------------------------

chunks = []
vectors = None

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 3),
    max_features=5000
)

# -----------------------------
# CLEAN TEXT
# -----------------------------

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# -----------------------------
# SMART CHUNKING
# -----------------------------

def create_chunks(text, chunk_size=800):

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

    global chunks, vectors

    chunks = []

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:

        text = page.get_text("text")

        full_text += text + "\n"

    full_text = clean_text(full_text)

    if len(full_text) < 20:
        return "No readable text found"

    # Create chunks
    chunks = create_chunks(full_text)

    chunks = [c for c in chunks if len(c) > 50]

    if len(chunks) == 0:
        return "No valid chunks generated"

    # Create vectors
    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"

# -----------------------------
# ASK QUESTION
# -----------------------------

def ask_question(query):

    global chunks, vectors

    if vectors is None:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        vectors
    )[0]

    top_indices = similarities.argsort()[-5:][::-1]

    query_words = query.lower().split()

    best_results = []

    for idx in top_indices:

        chunk = chunks[idx]

        score = similarities[idx]

        keyword_matches = 0

        for word in query_words:

            if word in chunk.lower():
                keyword_matches += 1

        final_score = score + (keyword_matches * 0.1)

        best_results.append((final_score, chunk))

    best_results = sorted(
        best_results,
        reverse=True
    )

    final_answers = []

    for score, chunk in best_results[:2]:

        if score > 0.15:
            final_answers.append(chunk)

    if len(final_answers) == 0:
        return "Answer not found in document"

    return "\n\n".join(final_answers)
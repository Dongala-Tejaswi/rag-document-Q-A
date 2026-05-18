import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

chunks = []
vectorizer = TfidfVectorizer(stop_words="english")
vectors = None


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def process_pdf(file_path):
    global chunks, vectors

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    text = clean_text(text)

    # Better chunk splitting
    raw_chunks = re.split(r'(?<=\.)\s+', text)

    chunks = []

    current_chunk = ""

    for sentence in raw_chunks:

        if len(current_chunk) + len(sentence) < 500:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    chunks = [c for c in chunks if len(c) > 40]

    if len(chunks) == 0:
        return "No text extracted from PDF"

    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):
    global chunks, vectors

    if vectors is None or len(chunks) == 0:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, vectors).flatten()

    best_match_index = similarities.argmax()

    best_score = similarities[best_match_index]

    if best_score < 0.1:
        return "No relevant answer found in document"

    answer = chunks[best_match_index]

    return answer
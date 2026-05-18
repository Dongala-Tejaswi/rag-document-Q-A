import fitz
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

chunks = []

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 3),
    max_features=5000
)

vectors = None


def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


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


def process_pdf(file_path):

    global chunks, vectors

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:

        text = page.get_text("text")

        full_text += text + "\n"

    full_text = clean_text(full_text)

    if len(full_text) < 20:
        return "No readable text found"

    chunks = create_chunks(full_text)

    chunks = [chunk for chunk in chunks if len(chunk) > 50]

    if len(chunks) == 0:
        return "No valid text chunks found"

    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):

    global chunks, vectors

    if vectors is None:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        vectors
    )[0]

    best_index = similarities.argmax()

    best_score = similarities[best_index]

    if best_score < 0.08:
        return "Answer not found in document"

    return chunks[best_index]
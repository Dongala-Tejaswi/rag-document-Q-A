import fitz
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

chunks = []
vectors = None

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=15000
)


def clean_text(text):

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def chunk_text(text, chunk_size=500):

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
        return "No readable text found in PDF"

    # Smart semantic chunks
    chunks = chunk_text(full_text)

    chunks = [chunk for chunk in chunks if len(chunk) > 50]

    if len(chunks) == 0:
        return "No valid chunks generated"

    # Create embeddings
    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):

    global chunks, vectors

    if vectors is None or len(chunks) == 0:
        return "Please upload PDF first"

    query = clean_text(query)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, vectors).flatten()

    # Get top 3 most relevant chunks
    top_indices = similarities.argsort()[-3:][::-1]

    results = []

    for idx in top_indices:

        score = similarities[idx]

        if score > 0.05:
            results.append(chunks[idx])

    if len(results) == 0:
        return "Answer not found in document"

    final_answer = "\n\n".join(results)

    return final_answer
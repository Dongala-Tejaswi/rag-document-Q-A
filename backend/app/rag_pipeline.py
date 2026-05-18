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
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_pdf(file_path):

    global chunks, vectors

    chunks = []

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:
        text = page.get_text("text")
        full_text += text + "\n"

    full_text = clean_text(full_text)

    # Better intelligent chunking
    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) < 600:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Remove tiny chunks
    chunks = [chunk for chunk in chunks if len(chunk) > 50]

    if len(chunks) == 0:
        return "No text extracted from PDF"

    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):

    global chunks, vectors

    if vectors is None or len(chunks) == 0:
        return "Please upload PDF first"

    query = clean_text(query)

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, vectors).flatten()

    best_indices = similarities.argsort()[-3:][::-1]

    answers = []

    for idx in best_indices:

        score = similarities[idx]

        if score > 0.05:
            answers.append(chunks[idx])

    if len(answers) == 0:
        return "Answer not found in document"

    final_answer = "\n\n".join(answers)

    return final_answer
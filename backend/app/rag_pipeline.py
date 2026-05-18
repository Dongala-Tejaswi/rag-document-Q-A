import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

chunks = []
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)
vectors = None


def process_pdf(file_path):

    global chunks, vectors

    chunks = []

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:
        text = page.get_text("text")
        full_text += text + "\n"

    full_text = full_text.replace("\n", " ")

    chunk_size = 400

    for i in range(0, len(full_text), chunk_size):

        chunk = full_text[i:i + chunk_size]

        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())

    if len(chunks) == 0:
        return "No text extracted from PDF"

    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):

    global chunks, vectors

    if vectors is None or len(chunks) == 0:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, vectors)

    best_index = similarities.argmax()

    best_score = similarities[0][best_index]

    # similarity threshold
    if best_score < 0.05:
        return "Answer not found in document"

    answer = chunks[best_index]

    return answer
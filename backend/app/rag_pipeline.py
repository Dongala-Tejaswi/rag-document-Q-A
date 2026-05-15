import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

chunks = []
vectorizer = TfidfVectorizer(stop_words='english')
vectors = None


def process_pdf(file_path):
    global chunks, vectors

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    # Better chunking
    raw_chunks = text.split("\n\n")

    chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()

        if len(chunk) > 30:
            chunks.append(chunk)

    if len(chunks) == 0:
        return "No text extracted"

    vectors = vectorizer.fit_transform(chunks)

    return "PDF uploaded successfully"


def ask_question(query):
    global chunks, vectors

    if vectors is None:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, vectors)

    best_index = similarities.argmax()

    answer = chunks[best_index]

    return answer
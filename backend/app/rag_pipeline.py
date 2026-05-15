import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = []
vectorizer = TfidfVectorizer()

vectors = None


def process_pdf(file_path):
    global documents, vectors

    doc = fitz.open(file_path)

    text = ""

    for page in doc:
        text += page.get_text()

    # Split into chunks
    documents = text.split("\n")

    # Remove empty lines
    documents = [doc.strip() for doc in documents if doc.strip()]

    if len(documents) > 0:
        vectors = vectorizer.fit_transform(documents)

    return "PDF processed successfully"


def ask_question(query):
    global documents, vectors

    if vectors is None or len(documents) == 0:
        return "No PDF uploaded yet."

    query_vector = vectorizer.transform([query])

    similarity = cosine_similarity(query_vector, vectors)

    index = similarity.argmax()

    return documents[index]
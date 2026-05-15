import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = []
vectorizer = TfidfVectorizer()
vectors = None


def process_pdf(file_path):
    global documents, vectors

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    documents = text.split("\n")

    documents = [d.strip() for d in documents if d.strip()]

    if len(documents) == 0:
        return "No text found in PDF"

    vectors = vectorizer.fit_transform(documents)

    return "PDF uploaded successfully"


def ask_question(query):
    global documents, vectors

    if vectors is None:
        return "Please upload PDF first"

    query_vector = vectorizer.transform([query])

    similarity = cosine_similarity(query_vector, vectors)

    index = similarity.argmax()

    return documents[index]
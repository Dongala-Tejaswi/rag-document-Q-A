import fitz
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
embeddings = []
def process_pdf(file_path):
    global documents, embeddings

    documents = []
    embeddings = []

    pdf = fitz.open(file_path)

    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    pdf.close()

    # Split into chunks
    chunks = full_text.split("\n")

    for chunk in chunks:
        chunk = chunk.strip()

        if len(chunk) > 20:
            documents.append(chunk)

            embedding = model.encode(chunk).tolist()

            embeddings.append(embedding)

    return {"message": "PDF processed successfully"}


def ask_question(query):
    global documents, embeddings

    if len(documents) == 0 or len(embeddings) == 0:
        return "No PDF uploaded or processed."

    query_embedding = model.encode(query).reshape(1, -1)

    embeddings_array = np.array(embeddings)

    similarities = cosine_similarity(query_embedding, embeddings_array)

    best_match_index = similarities.argmax()

    answer = documents[best_match_index]

    return answer
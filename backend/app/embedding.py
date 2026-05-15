from app.embedding import create_embedding
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
stored_vectors = None

def create_embedding(texts):
    global stored_vectors

    if stored_vectors is None:
        stored_vectors = vectorizer.fit_transform(texts)
        return stored_vectors.toarray()

    return vectorizer.transform(texts).toarray()
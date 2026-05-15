from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
stored_vectors = None
def create_embedding(texts):
    global stored_vectors
    vectors = vectorizer.fit_transform(texts)
    stored_vectors = vectors
    return vectors.toarray()
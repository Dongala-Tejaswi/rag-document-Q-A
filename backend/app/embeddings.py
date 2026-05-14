from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

def create_embedding(texts):
    return vectorizer.fit_transform(texts).toarray().tolist()
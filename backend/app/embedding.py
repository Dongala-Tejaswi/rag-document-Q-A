from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

is_fitted = False


def create_embedding(texts):

    global is_fitted

    if not is_fitted:
        vectors = vectorizer.fit_transform(texts)
        is_fitted = True
    else:
        vectors = vectorizer.transform(texts)

    return vectors.toarray()
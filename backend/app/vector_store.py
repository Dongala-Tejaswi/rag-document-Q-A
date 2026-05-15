from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

stored_chunks = []
stored_embeddings = []


def store_embeddings(chunks, embeddings):
    global stored_chunks, stored_embeddings

    stored_chunks = chunks
    stored_embeddings = embeddings


def search_embeddings(query_embedding):

    global stored_chunks, stored_embeddings

    if len(stored_embeddings) == 0:
        return []

    similarities = cosine_similarity(
        [query_embedding],
        stored_embeddings
    )[0]

    top_indices = np.argsort(similarities)[-5:][::-1]

    return [stored_chunks[i] for i in top_indices]
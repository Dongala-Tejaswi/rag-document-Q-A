from sklearn.metrics.pairwise import cosine_similarity
from app.embedding import create_embedding
import numpy as np

stored_chunks = []
stored_embeddings = []


def store_embeddings(chunks, embeddings):
    global stored_chunks, stored_embeddings

    stored_chunks = chunks
    stored_embeddings = embeddings


def search_embeddings(query, top_k=3):
    global stored_chunks, stored_embeddings

    query_embedding = create_embedding([query])

    similarities = cosine_similarity(
        query_embedding,
        stored_embeddings
    )[0]

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    results = [stored_chunks[i] for i in top_indices]

    return results
from sklearn.metrics.pairwise import cosine_similarity
from app.embedding import create_embedding

stored_chunks = []
stored_embeddings = []


def store_embeddings(chunks, embeddings):
    global stored_chunks, stored_embeddings

    stored_chunks = chunks
    stored_embeddings = embeddings


def search_embeddings(query):
    global stored_chunks, stored_embeddings

    if not stored_embeddings:
        return []

    query_embedding = create_embedding([query])

    similarities = cosine_similarity(
        query_embedding,
        stored_embeddings
    )[0]

    top_indices = similarities.argsort()[-5:][::-1]

    results = [stored_chunks[i] for i in top_indices]

    return results
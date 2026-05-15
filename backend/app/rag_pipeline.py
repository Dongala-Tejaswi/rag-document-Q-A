from app.pdf_utils import extract_text
from app.embeddings import create_embedding
from app.vector_store import store_embeddings, search
from app.llm import generate_answer


# Better text chunking
def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


def process_pdf(file_path):

    text = extract_text(file_path)

    # Better chunks
    chunks = chunk_text(text)

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)

    print("PDF processed successfully")


def ask_question(query):

    query_embedding = create_embedding([query])[0]

    # Retrieve top relevant chunks
    results = search(query_embedding)

    context = "\n".join(results)

    print("Retrieved Context:")
    print(context)

    answer = generate_answer(context, query)

    return answer
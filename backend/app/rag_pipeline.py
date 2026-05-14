from app.pdf_utils import extract_text
from app.embeddings import create_embedding
from app.vector_store import store_embeddings, search
from app.llm import generate_answer

def chunk_text(text, size=500):

    chunks = []

    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])

    return chunks

def process_pdf(path):

    text = extract_text(path)

    chunks = chunk_text(text)

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)

def ask_question(query):

    query_embedding = create_embedding([query])[0]

    docs = search(query_embedding)

    context = "\n".join(docs)

    answer = generate_answer(context, query)

    return answer
from app.pdf_utils import extract_text
from app.embedding import create_embedding
from app.vector_store import store_embeddings, search_embeddings
from app.llm import generate_answer

all_chunks = []

def split_text(text, chunk_size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def process_pdf(pdf_path):
    global all_chunks

    text = extract_text(pdf_path)

    chunks = split_text(text)

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)

    all_chunks.extend(chunks)

    return "PDF processed successfully"

def ask_question(query):
    results = search_embeddings(query)
    context = "\n".join(results)
    answer = generate_answer(context, query)
    return answer
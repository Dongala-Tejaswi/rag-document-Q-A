from app.pdf_utils import extract_text
from app.embeddings import create_embedding
from app.vector_store import store_embeddings, search
from app.llm import generate_answer


def process_pdf(pdf_path):
    text = extract_text(pdf_path)

    # Split text into chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)

    return "PDF processed successfully"


def ask_question(query):
    query_embedding = create_embedding([query])[0]

    docs = search(query_embedding)

    context = "\n".join(docs)

    answer = generate_answer(context, query)

    return answer
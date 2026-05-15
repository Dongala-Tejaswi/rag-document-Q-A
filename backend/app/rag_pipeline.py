import fitz

from app.embedding import create_embedding
from app.vector_store import store_embeddings, search
from app.llm import generate_answer


def extract_text_from_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)


def ask_question(query):
    query_embedding = create_embedding([query])[0]

    context = search(query_embedding)

    answer = generate_answer(context, query)

    return answer
from app.pdf_utils import extract_text
from app.embeddings import create_embedding
from app.vector_store import store_embeddings, search
from app.llm import generate_answer


def process_pdf(file_path):

    text = extract_text(file_path)

    chunks = text.split("\n")

    chunks = [chunk for chunk in chunks if chunk.strip() != ""]

    embeddings = create_embedding(chunks)

    store_embeddings(chunks, embeddings)


def ask_question(query):

    query_embedding = create_embedding([query])[0]

    results = search(query_embedding)

    context = "\n".join(results)

    answer = generate_answer(context, query)

    return answer
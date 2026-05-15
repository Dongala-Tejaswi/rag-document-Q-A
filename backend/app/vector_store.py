import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="documents"
)

doc_count = 0


def store_embeddings(chunks, embeddings):

    global doc_count

    for i, chunk in enumerate(chunks):

        collection.add(
            ids=[str(doc_count)],
            documents=[chunk],
            embeddings=[embeddings[i]]
        )

        doc_count += 1

    print("Stored embeddings:", doc_count)


def search(query_embedding):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    print(results)

    documents = results["documents"][0]

    return " ".join(documents)
from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(context, question):

    prompt = f"""
You are a resume assistant.

Answer ONLY from the provided context.

If the answer exists in the context, return it clearly.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content
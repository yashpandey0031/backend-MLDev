from main import build_vectorstore
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

query = input("Ask a question about the pdf: ")

vectorstore = build_vectorstore("pdf/SystemDesignInterview.pdf")

results = vectorstore.similarity_search(query, k=3)

context = "\n\n".join([r.page_content for r in results])

prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {query}
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
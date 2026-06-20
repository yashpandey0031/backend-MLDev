import os
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from services.rag import get_vectorstore, has_vectorstore

load_dotenv()
router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = []

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    if not has_vectorstore():
        return {"error": "No PDF uploaded yet"}

    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(req.question, k=3)
    context = "\n\n".join([r.page_content for r in results])

    history_text = ""
    for turn in chat_history[-5:]:
        history_text += f"User: {turn['question']}\nAssistant: {turn['answer']}\n\n"

    prompt = f"""Answer using only the context below. If not found, say you don't know.

Previous conversation:
{history_text}

Context:
{context}

Question: {req.question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    chat_history.append({"question": req.question, "answer": answer})

    return {"answer": answer}
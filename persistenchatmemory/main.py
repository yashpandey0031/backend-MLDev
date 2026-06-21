import chromadb 
from chromadb.utils import embedding_functions
import uuid
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))




embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path="./chroma_memory") #connection to the chroma database 

#if a collectino or table called chat_memory already exists open it otherwise create it fresh
collection = chroma_client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_fn
)

# collection.add(
#   ids = ["msg1"],
#   documents=["something something"],
#   metadata=[{"timestamp":"2026-06-21"}]
# )

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Search Chroma for similar past memories
    results = collection.query(
        query_texts=[user_input],
        n_results=3
    )
    past_memories = results["documents"][0]  # list of matched strings

    memory_text = "\n".join(past_memories) if past_memories else "(no relevant memories)"
#Builds the actual prompt — same "grounding" concept from your RAG project, except instead of grounding in a PDF, you're grounding in past conversation history.
    prompt = f"""You are a chatbot with memory of past conversations. Use the memories below if relevant.

Past memories:
{memory_text}

Current message: {user_input}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    print(f"Bot: {answer}")

    # Store this exchange as a new memory
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[f"User said: {user_input}. Bot replied: {answer}"],
        metadatas=[{"timestamp": "2026-06-21"}]
    )
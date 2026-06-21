import chromadb



embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path="./chroma_memory") #connection to the chroma database 

#if a collectino or table called chat_memory already exists open it otherwise create it fresh
collection = chroma_client.get_or_create_collection(
    name="chat_memory",
    embedding_function=embedding_fn
)

collection.add(
  ids = ["msg1"]
  documents=["something something"]
  metadata=[{"timestamp":"2026-06-21"}]
)
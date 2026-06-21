import chromadb
chroma_client = chromadb.PersistentClient(path="./chroma_memory") #connection to the chroma database 

#if a collectino or table called chat_memory already exists open it otherwise create it fresh
collection = chroma_client.get_or_create_collection(name="chat_memory")


collection.add(
  ids = ["msg1"]
  documents=["something something"]
  metadata=[{"timestamp":"2026-06-21"}]
)
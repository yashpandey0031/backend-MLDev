from langchain_community.document_loaders import PyPDFLoader #its function is for loading 
from langchain_text_splitters import RecursiveCharacterTextSplitter #its function is splitting
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
#fullform of faiss

loader = PyPDFLoader("pdf/SystemDesignInterview.pdf")

print(len(loader.load()))
pages = loader.load()
# print(pages[1].page_content)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

chunks =  splitter.split_documents(pages)

embeddings = HuggingFaceEmbeddings(model_name = "sentence-tranformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_documents(chunks, embeddings)


results = vectorstore.similarity_search("How does the notification system work?", k=3)

for r in results:
    print(r.page_content)
    print("---")
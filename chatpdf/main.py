from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def build_vectorstore(pdf_path):
    loader = PyPDFLoader(pdf_path) #load the pdf
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) #split the pdf into chunks
    chunks = splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #create embeddings and store them into a vectorstore
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore
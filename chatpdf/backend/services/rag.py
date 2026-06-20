import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_PATH = "faiss_index"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

_vectorstore = None

def build_vectorstore(pdf_path):
    global _vectorstore

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)

    _vectorstore = FAISS.from_documents(chunks, embeddings)
    _vectorstore.save_local(INDEX_PATH)

    return _vectorstore

def get_vectorstore():
    return _vectorstore

def has_vectorstore():
    return _vectorstore is not None
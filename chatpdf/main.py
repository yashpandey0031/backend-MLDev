from langchain_community.document_loaders import PyPDFLoader #its function is for loading 
from langchain_text_splitters import RecursiveCharacterTextSplitter #its function is splitting

loader = PyPDFLoader("pdf/SystemDesignInterview.pdf")

print(len(loader.load()))
pages = loader.load()
print(pages[1].page_content)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

print(len(splitter.split_documents(pages)))


from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("pdf/SystemDesignInterview.pdf")

print(loader.load(total_pages))


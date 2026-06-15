from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("pdf/SystemDesignInterview.pdf")

print(len(loader.load()))
pages = loader.load()
print(pages[1].page_content)
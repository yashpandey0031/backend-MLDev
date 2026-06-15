from langchain_community.document_loaders import PyPDFLoader,RecursiveCharacterTextSplitter

loader = PyPDFLoader("pdf/SystemDesignInterview.pdf")

print(len(loader.load()))
pages = loader.load()
print(pages[1].page_content)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

splitter.split_documents()


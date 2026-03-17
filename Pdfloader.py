from langchain_community.document_loaders import PyPDFLoader
 
 
def load_pdf(file_path):
    """Load and return documents from a PDF file."""
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []

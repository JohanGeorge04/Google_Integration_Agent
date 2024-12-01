from langchain.tools import tool
from app import get_credentials
from create import create_google_doc

@tool
def create_and_store_doc_tool(input_text: str) -> str:
    """Creates a Google Doc and stores it in Google Drive."""
    creds = get_credentials()
    doc_url = create_google_doc("New Document", input_text, creds)
    return f"Document created and stored: {doc_url}"

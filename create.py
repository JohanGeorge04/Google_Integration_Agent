from googleapiclient.discovery import build
from app import get_credentials

def find_doc_by_title(title: str):
    """Searches for a document by its title in Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Use the Drive API to list files with the specified title
    results = service.files().list(
        q=f"name='{title}' and mimeType='application/vnd.google-apps.document'",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    
    if not files:
        return None  # Document not found
    return files[0]['id']  # Return the first matching document ID

def create_document(title: str, content: str):
    """Create a new Google Doc."""
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId")
    service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": content,
                    }
                }
            ]
        }
    ).execute()
    return f"Document created: https://docs.google.com/document/d/{doc_id}"

def update_document(title: str, content: str):
    """Update a Google Doc by its title."""
    doc_id = find_doc_by_title(title)
    if not doc_id:
        return f"No document found with the title '{title}'."
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)
    service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": content,
                    }
                }
            ]
        }
    ).execute()
    return f"Document updated: https://docs.google.com/document/d/{doc_id}"

def delete_document(title: str):
    """Delete a Google Doc by its title."""
    doc_id = find_doc_by_title(title)
    if not doc_id:
        return f"No document found with the title '{title}'."
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)
    service.files().delete(fileId=doc_id).execute()
    return f"Document with title '{title}' deleted successfully."

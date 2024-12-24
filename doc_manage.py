from googleapiclient.discovery import build
from credential import get_credentials

def find_doc_by_title(title: str):
    """Searches for a document by its title in Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        q=f"name='{title}' and mimeType='application/vnd.google-apps.document' and trashed=false",
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    
    if not files:
        return None  
    return files[0]['id'] 

def create_document(title: str, content: str, folder_id: str):
    """
    Create a new Google Doc. If a document with the same title exists, return its link.
    """
    
    existing_doc_id = find_doc_by_title(title)  
    if existing_doc_id:
        return f"Document with the title '{title}' already exists: https://docs.google.com/document/d/{existing_doc_id}"

    creds = get_credentials()  
    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
 
    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId")

    docs_service.documents().batchUpdate(
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
  
    file_metadata = {
        "name": title,
        "parents": [folder_id]  
    }
    drive_service.files().update(fileId=doc_id, addParents=folder_id).execute()

    return f"Document created: https://docs.google.com/document/d/{doc_id}"

def update_document(title: str, content: str):
    """
    Update a Google Doc by first clearing its content and then adding new content.
    """
   
    doc_id = find_doc_by_title(title)  
    if not doc_id:
        return f"No document found with the title '{title}'."

    creds = get_credentials()  
    service = build("docs", "v1", credentials=creds)
   
    document = service.documents().get(documentId=doc_id).execute()
    doc_length = document.get('body').get('content')[-1].get('endIndex', 1)  
   
    service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
            
                {
                    "deleteContentRange": {
                        "range": {
                            "startIndex": 1,
                            "endIndex": doc_length - 1  
                        }
                    }
                },
           
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
    """
    Delete a Google Doc by title.
    """
    doc_id = find_doc_by_title(title)  
    if not doc_id:
        return f"No document found with the title '{title}'."
    creds = get_credentials() 
    service = build("drive", "v3", credentials=creds)
    service.files().delete(fileId=doc_id).execute()

    return f"Document with title '{title}' deleted successfully."
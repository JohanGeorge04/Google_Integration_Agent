from googleapiclient.discovery import build
from app import get_credentials

def create_google_doc(title, content, creds):
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc.get('documentId')
    service.documents().batchUpdate(documentId=doc_id, body={
        'requests': [
            {'insertText': {'location': {'index': 1}, 'text': content}}
        ]
    }).execute()
    return f"https://docs.google.com/document/d/{doc_id}"

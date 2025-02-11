from langchain.tools import BaseTool
from langchain.schema import Document  
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from googleapiclient.discovery import build
import os
from credential import get_credentials
from typing import List

class GoogleDocsRetrieverTool(BaseTool):
    name: str = "google_docs_retriever"
    description: str = "Fetches Google Docs, extracts text, and retrieves relevant information based on user query."
    
    def _run(self, query: str) -> List[str]:
        if not query:
            raise ValueError("Query cannot be empty. Please provide a search term.")
        
        credentials = get_credentials()
        drive_service = build("drive", "v3", credentials=credentials)
        docs_service = build("docs", "v1", credentials=credentials)
        
        # Fetch Google Docs
        def get_all_google_docs():
            query = "mimeType='application/vnd.google-apps.document' and trashed=false"
            files = []
            page_token = None
            while True:
                response = drive_service.files().list(
                    q=query,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token
                ).execute()
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken")
                if not page_token:
                    break
            return files
        
        # Extract text from Google Docs
        def extract_text_from_google_doc(doc_id):
            document = docs_service.documents().get(documentId=doc_id).execute()
            content = []
            for element in document.get("body", {}).get("content", []):
                if "paragraph" in element:
                    for para_element in element["paragraph"]["elements"]:
                        if "textRun" in para_element:
                            content.append(para_element["textRun"]["content"])
            return "".join(content).strip()
        
        google_docs = get_all_google_docs()
        if not google_docs:
            raise ValueError("No Google Docs found in Google Drive.")
        
        documents = []
        for file in google_docs:
            try:
                text = extract_text_from_google_doc(file["id"])
                if text:
                    documents.append({"title": file["name"], "page_content": text})
            except Exception as e:
                print(f"Skipping {file['name']} due to error: {e}")
        
        docs = [Document(page_content=doc["page_content"], metadata={"title": doc["title"]}) for doc in documents]  
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(docs)
        docs = [doc for doc in docs if doc.page_content.strip()]
        
        if not docs:
            raise ValueError("No valid documents found after processing.")
        
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/embedding-001")
        vector_db = FAISS.from_documents(docs, embeddings)
        
        retriever = vector_db.as_retriever(top_k=3)
        retrieved_docs = retriever.get_relevant_documents(query)
        
        if not retrieved_docs:
            return ["No relevant content found for your query."]
        
        return [doc.page_content for doc in retrieved_docs]

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
    description: str = "Fetches Google Docs, finds the most relevant document, extracts key information, and answers the query using LLM."

    def _run(self, query: str) -> str:
        if not query:
            raise ValueError("Query cannot be empty. Please provide a search term.")
        
        credentials = get_credentials()
        drive_service = build("drive", "v3", credentials=credentials)
        docs_service = build("docs", "v1", credentials=credentials)
        
        #  Fetch Google Docs list
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
        
        #  Extract full text from a Google Doc (Caching Enabled)
        cache = {}  # Dictionary to store fetched documents
        def extract_text_from_google_doc(doc_id):
            if doc_id in cache:
                return cache[doc_id]  # Return cached content to avoid redundant API calls
            document = docs_service.documents().get(documentId=doc_id).execute()
            content = []
            for element in document.get("body", {}).get("content", []):
                if "paragraph" in element:
                    for para_element in element["paragraph"]["elements"]:
                        if "textRun" in para_element:
                            content.append(para_element["textRun"]["content"])
            text = "".join(content).strip()
            cache[doc_id] = text  # Store in cache
            return text
        
        google_docs = get_all_google_docs()
        if not google_docs:
            raise ValueError("No Google Docs found in Google Drive.")
        
        #  Load text from Google Docs
        documents = []
        for file in google_docs:
            try:
                text = extract_text_from_google_doc(file["id"])
                if text:
                    documents.append({"title": file["name"], "page_content": text, "id": file["id"]})
            except Exception as e:
                print(f"Skipping {file['name']} due to error: {e}")
        
        #  Convert extracted text into LangChain format
        docs = [Document(page_content=doc["page_content"], metadata={"title": doc["title"], "id": doc["id"]}) for doc in documents]  
        
        #  Improved Chunking (Sentence-based + Recursive)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(docs)
        docs = [doc for doc in docs if doc.page_content.strip()]
        
        if not docs:
            raise ValueError("No valid documents found after processing.")
        
        #  Generate embeddings and store in FAISS
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.getenv("GEMINI_API_KEY"), model="models/embedding-001")
        vector_db = FAISS.from_documents(docs, embeddings)

        #  Query Expansion using MultiQueryRetriever
        llm = ChatGoogleGenerativeAI(google_api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.0-flash", temperature=0)
        retriever = MultiQueryRetriever.from_llm(retriever=vector_db.as_retriever(top_k=3), llm=llm)

        # Retrieve top-ranked document
        retrieved_docs = retriever.invoke(query)
        if not retrieved_docs:
            return "No relevant document found."

        #  Extract full content of the most relevant document
        top_doc_metadata = retrieved_docs[0].metadata
        doc_id = top_doc_metadata["id"]
        full_content = extract_text_from_google_doc(doc_id)

        #  Secondary Chunking & Retrieval
        doc_chunks = text_splitter.split_text(full_content)
        doc_objects = [Document(page_content=chunk) for chunk in doc_chunks]
        doc_vector_db = FAISS.from_documents(doc_objects, embeddings)
        relevant_chunks = doc_vector_db.similarity_search(query, k=3)  # Get top 3 relevant chunks

        if not relevant_chunks:
            return "No relevant content found in the document."

        #  Answer the query using LLM
        extracted_text = "\n".join([chunk.page_content for chunk in relevant_chunks])
        final_prompt = f"Answer the following question based on the extracted document:\n\nQuestion: {query}\n\nExtracted Content: {extracted_text}\n\nAnswer:"

        response = llm.invoke(final_prompt)
        return response.content.strip() 
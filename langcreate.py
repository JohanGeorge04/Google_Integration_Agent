from langchain.tools import tool
from app import get_credentials
from create import create_document,update_document,delete_document
import json


@tool
def create_doc(input_text: str) -> str:
    """
    Create a Google Doc.
    Input format (JSON): {"title": "<title>", "content": "<content>"}
    """
    try:
        data = json.loads(input_text)

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        if not title or not content:
            return "Error: Both 'title' and 'content' fields are required."
        return create_document(title, content)  
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide input as JSON: {'title': '<title>', 'content': '<content>'}"

@tool
def update_doc(input_text: str) -> str:
    """
    Update a Google Doc.
    Input format (JSON): {"title": "<title>", "content": "<content>"}
    """
    try:
        data = json.loads(input_text)

        title = data.get("title", "").strip()
        content = data.get("content", "").strip()

        if not title or not content:
            return "Error: Both 'title' and 'content' fields are required."
        return update_document(title, content)
    
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide input as JSON: {'title': '<title>', 'content': '<content>'}"


@tool
def delete_doc(input_text: str) -> str:
    """
    Delete a Google Doc.
    Input format: 'Document title'
    """
    try:
    
        title = input_text.split("'")[1]
        title = title.strip()
        return delete_document(title)
       
    
    except IndexError:
        return "Error: Please provide the title of the document in the correct format."
    except Exception as e:
        return f"An error occurred: {e}"



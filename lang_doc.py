from langchain.tools import tool
from doc_manage import create_document, update_document, delete_document
from lang_folder import get_selected
import json

@tool
def create_doc(input_text: str) -> str:
    """
    Create a Google Doc.
    Input format (JSON): {"title": "<title>", "content": "<content>"}
    """
    selected_folder = get_selected()
    if not selected_folder["id"]:
        return "Error: No folder selected. Please select a folder first."
    try:
        data = json.loads(input_text)
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        if not title or not content:
            return "Error: Both 'title' and 'content' fields are required."
        create_document(title, content, selected_folder["id"])
        return f"Document '{title}' created successfully in folder '{selected_folder['name']}'."
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
        title = input_text.strip()
        return delete_document(title)
    except IndexError:
        return "Error: Please provide the title of the document in the correct format."
    except Exception as e:
        return f"An error occurred: {e}"

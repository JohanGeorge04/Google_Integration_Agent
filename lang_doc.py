from langchain.tools import tool
from doc_manage import create_document, update_document, delete_document,add_content_to_document,find_doc_by_title,get_document_content

from lang_folder import get_selected
import json


last_created_document = {"id": None, "title": None}

@tool
def create_doc(input_text: str) -> str:
    """
    Create a Google Doc with a title.
    Input format (JSON): {"title": "<title>"}
    """
    global last_created_document
    selected_folder = get_selected()
    if not selected_folder.get("id"):
        return "Error: No folder selected. Please select a folder first."
    
    try:
        data = json.loads(input_text)
        title = data.get("title", "").strip()
        
        if not title:
            return "Error: The 'title' field is required."
        
        # Create the document
        document_id, document_url = create_document(title, selected_folder["id"])
        last_created_document = {"id": document_id, "title": title}
        
        # Prompt the user if they want to add content
        while True:
            add_content_choice = input("Do you want to add content to the document? (yes/no): ").strip().lower()
            if add_content_choice in ('yes', 'no'):
                break
            print("Invalid input. Please enter 'yes' or 'no'.")
        
        # If user chooses to add content, prompt for it
        if add_content_choice == 'yes':
            content = input("Enter the content to be added to the document: ").strip()
            if content:
                add_content_to_document(document_id, content)
                return (f"Document '{title}' created successfully with ID '{document_id}' "
                        f"in folder '{selected_folder['name']}', and content added. "
                        f"View the document here: {document_url}")
            else:
                return (f"Document '{title}' created successfully with ID '{document_id}' "
                        f"in folder '{selected_folder['name']}', but no content was added. "
                        f"View the document here: {document_url}")
        
        # If user chooses not to add content
        return (f"Document '{title}' created successfully with ID '{document_id}' "
                f"in folder '{selected_folder['name']}'. No content was added. "
                f"View the document here: {document_url}")
    
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide input as JSON: {\"title\": \"<title>\"}."
    except Exception as e:
        return f"An error occurred: {e}"
@tool
def create_doc_with_content(input_text: str) -> str:
    """
    Create a Google Doc with a title and content.
    Input format (JSON): {"title": "<title>", "content": "<content>"}
    """
    global last_created_document
    selected_folder = get_selected()
    if not selected_folder.get("id"):
        return "Error: No folder selected. Please select a folder first."
    
    try:
        data = json.loads(input_text)
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        
        if not title:
            return "Error: The 'title' field is required."
        
        document_id, document_url = create_document(title, selected_folder["id"])
        last_created_document = {"id": document_id, "title": title}
        
        if content:
            add_content_to_document(document_id, content)
            return (f"Document '{title}' created successfully with ID '{document_id}' "
                    f"in folder '{selected_folder['name']}', and content added. "
                    f"View the document here: {document_url}")
        
        return (f"Document '{title}' created successfully with ID '{document_id}' "
                f"in folder '{selected_folder['name']}', but no content was added. "
                f"View the document here: {document_url}")
    
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide input as JSON: {\"title\": \"<title>\", \"content\": \"<content>\"}."
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def update_doc(input_text: str) -> str:
    """
    Update a Google Doc by title.
    Input format (JSON): {"title": "<title>"}
    """
    try:
        data = json.loads(input_text)
        title = data.get("title", "").strip()

        if not title:
            return "Error: The 'title' field is required."

        # Locate the document by title
        document_id = find_doc_by_title(title)

        if not document_id:
            return f"Error: Document with title '{title}' not found."

        while True:
            action_choice = input("Do you want to overwrite the content? (yes to overwrite / no to append): ").strip().lower()
            if action_choice in ('yes', 'no'):
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        content = input("Enter the new content for the document: ").strip()

        if not content:
            return "Error: No content provided for updating the document."

        if action_choice == 'yes':
            # Overwrite the document's content
            update_document(title, content)
            action_taken = "overwritten"
        else:
            # Append to the document's content
            current_content = get_document_content(document_id)
            new_content = current_content + "\n" + content
            update_document(title, new_content)
            action_taken = "appended to"

        return f"Document '{title}' successfully {action_taken} with new content."

    
    except json.JSONDecodeError:
        return "Error: Invalid JSON format. Please provide input as JSON: {\"title\": \"<title>\"}."
    except Exception as e:
        return f"An error occurred while updating the document: {e}"

@tool
def update_doc_with_content(input_text: str) -> str:
    """
    Update a Google Doc by title and content.
    Input format (JSON): {"title": "<title>", "content": "<content>"}
    """
    try:
        data = json.loads(input_text)
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        if not title or not content:
            return "Error: Both 'title' and 'content' fields are required."
        
       
        # Locate the document by title
        document_id = find_doc_by_title(title)

        if not document_id:
            return f"Error: Document with title '{title}' not found."

        while True:
            action_choice = input("Do you want to overwrite the content? (yes to overwrite / no to append): ").strip().lower()
            if action_choice in ('yes', 'no'):
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        content = input("Enter the new content for the document: ").strip()

        if not content:
            return "Error: No content provided for updating the document."

        if action_choice == 'yes':
            # Overwrite the document's content
            update_document(title, content)
            action_taken = "overwritten"
        else:
            # Append to the document's content
            current_content = get_document_content(document_id)
            new_content = current_content + "\n" + content
            update_document(title, new_content)
            action_taken = "appended to"

        return f"Document '{title}' successfully {action_taken} with new content."
    except Exception as e:
        return f"An error occurred while updating the document: {e}"

@tool
def delete_doc(input_text: str) -> str:
    """
    Delete a Google Doc.
    Input format: 'Document title'
    """
    try:
        title = input_text.strip()
        if not title:
            return "Error: The document title is required."
        result = delete_document(title)
        return f"Document '{title}' deleted successfully."
    except Exception as e:
        return f"An error occurred while deleting the document: {e}"

@tool
def list_docs() -> str:
    """
    List all documents in the selected folder.
    """
    try:
        selected_folder = get_selected()
        if not selected_folder.get("id"):
            return "Error: No folder selected. Please select a folder first."
        documents = list_documents(selected_folder["id"])
        if not documents:
            return f"No documents found in folder '{selected_folder['name']}'."
        return "\n".join([f"- {doc['title']} (ID: {doc['id']})" for doc in documents])
    except Exception as e:
        return f"An error occurred while listing documents: {e}"

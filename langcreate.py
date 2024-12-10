from langchain.tools import tool
from app import get_credentials
from create import create_document,update_document,delete_document
import json


@tool
def create_doc(input_text: str) -> str:
    """
    Create a Google Doc.
    Input format: "Title: <title>, Content: <content>"
    """
    data = json.loads(input_text)

    title = data.get("Title", "").strip()
    content = data.get("Content", "").strip()
    return create_document(title, content)

@tool
def update_doc(input_text: str) -> str:
    """
    Update a Google Doc .
    Input format: "Title: <title>, Content: <content>"
    """
    title = input_text.split(":")[1].split(",")[0].strip()
    content = input_text.split(",")[1].split(":")[1].strip()
    return update_document(title, content)

@tool
def delete_doc(input_text: str) -> str:
    """
    Delete a Google Doc .
    Input format: "Title: <title>"
    """
    title = input_text.split(":")[1].split(",")[0].strip()
    return delete_document(title)

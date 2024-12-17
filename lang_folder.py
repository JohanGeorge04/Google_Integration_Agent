from langchain.tools import tool
import json
from folder_manage import create_drive_folder,delete_drive_folder

@tool
def create_folder(input_text: str) -> str:
    """
    Create a folder in Google Drive.
    Input format: <folder_name>
    """
    folder_name = input_text.strip()  
    if not folder_name:
        return "Error: Folder name is missing or empty."
    return create_drive_folder(folder_name)


@tool
def delete_folder(input_text: str) -> str:
    """
    Delete a folder in Google Drive.
    Input format: <folder_name>
    """
    folder_name = input_text.strip()  
    if not folder_name:
        return "Error: Folder name is missing or empty."
    return delete_drive_folder(folder_name)

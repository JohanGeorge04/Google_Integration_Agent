from langchain.tools import tool
import json
from folder_manage import create_drive_folder,delete_drive_folder,list_folders

selected_folder = {"id": "", "name": ""}

@tool
def create_folder(input_text: str) -> str:
    """
    Create a folder in Google Drive.
    Input format: <folder_name>
    """
    try:
        folder_name = input_text.strip()  
        if not folder_name:
            return "Error: Folder name is missing or empty."
        return create_drive_folder(folder_name)
    except Exception as e:
        return f"An error occurred: {e}"

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

@tool
def list_folders_tool(input_text: str = None) -> str:
    """
    List all available folders in Google Drive.No other operations are done.
    Input: No input required
    """
    try:   
        folders = list_folders()
        if isinstance(folders, list):
            return "\n".join([f"- {folder['name']} (ID: {folder['id']})" for folder in folders])
        else:
            return folders
    except Exception as e:
        return f"An error occurred while fetching folders: {e}"
    
@tool
def select_folder_tool(input_text: str) -> str:
    """
    Select a folder from the available list by name.
    Input format: <folder_name>
    """
    global selected_folder
    try:
        folders = list_folders()  
        for folder in folders:
            if folder["name"].lower() == input_text.lower():
                selected_folder = {"id": folder["id"], "name": folder["name"]}
                return f"Folder '{folder['name']}' selected successfully."
        return "Error: Folder not found. Please provide a valid folder name."
    except Exception as e:
        return f"An error occurred: {e}"

def get_selected():
    return selected_folder
    
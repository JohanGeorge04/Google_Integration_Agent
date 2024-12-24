from googleapiclient.discovery import build
from credential import get_credentials


def create_drive_folder(folder_name):
    """
    Creates a folder in Google Drive only if a folder with the same name doesn't already exist 
    and excludes trashed folders from the search.
    :param folder_name: Name of the folder to create.
    :return: Folder ID or a message indicating the folder already exists.
    """
    try:
        creds = get_credentials()
        drive_service = build("drive", "v3", credentials=creds)
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false and 'me' in owners"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        existing_folders = results.get("files", [])
     
        if existing_folders:
            return f"Folder with name '{folder_name}' already exists with ID: {existing_folders[0]['id']}"
   
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
   
        folder = drive_service.files().create(body=folder_metadata, fields="id").execute()
        return f"Folder '{folder_name}' created with ID: {folder.get('id')}"
    except Exception as e:
        return f"Failed to create folder: {e}"


def delete_drive_folder(folder_name: str):
    """
    Deletes a folder in Google Drive by its name (excluding trashed items).
    :param folder_name: Name of the folder to delete.
    :return: Success or error message.
    """
    try:

        creds = get_credentials()
        drive_service = build("drive", "v3", credentials=creds)
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false and 'me' in owners"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if not files:
            return f"Folder '{folder_name}' not found."
        for file in files:
            folder_id = file.get("id")
            try:
                drive_service.files().delete(fileId=folder_id).execute()
                print(f"Folder '{file.get('name')}' with ID '{folder_id}' deleted successfully.")
            except Exception as e:
                print(f"Failed to delete folder '{file.get('name')}' with ID '{folder_id}': {e}")

        return f"Deleted {len(files)} folder(s) named '{folder_name}'."
    except Exception as e:
        return f"Failed to delete folder: {e}"

def list_folders():
    """
    List all folders in the user's Google Drive.
    """
    try:
        creds = get_credentials()  
        service = build("drive", "v3", credentials=creds) 
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false and 'me' in owners",
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        folders = results.get("files", [])
        if not folders:
            return "No folders found."
        
        return [{"name": folder['name'], "id": folder['id']} for folder in folders]
    except Exception as e:
        
        return f"An error occurred: {e}"



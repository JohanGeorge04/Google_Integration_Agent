from googleapiclient.discovery import build
from app import get_credentials  # Import the function

def list_drive_files():
    """
    Lists the first 10 files in Google Drive.
    """
    creds = get_credentials()  # Get valid credentials
    service = build("drive", "v3", credentials=creds)

    # Call the Drive API
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    print("Files:")
    for item in items:
        print(f"{item['name']} ({item['id']})")

if __name__ == "__main__":
    list_drive_files()

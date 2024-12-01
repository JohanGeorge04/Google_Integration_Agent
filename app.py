import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the required scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents"
]

def get_credentials():
    """
    Handles Google API authentication and returns valid credentials.
    Saves a token.json file for reuse.
    """
    creds = None
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If credentials are not valid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for reuse
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

if __name__ == "__main__":
    get_credentials()

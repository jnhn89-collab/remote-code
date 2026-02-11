import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    
    # 1. Check for client_secrets.json (User must download this)
    if not os.path.exists('client_secrets.json'):
        print("Error: 'client_secrets.json' not found.")
        print("Please download your OAuth 2.0 Client ID JSON from Google Cloud Console.")
        print("Save it as 'client_secrets.json' in this folder.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', SCOPES)
    
    creds = flow.run_local_server(port=0)

    # Print the result in TOML format for secrets
    print("\n\nSUCCESS! Copy the following into your .streamlit/secrets.toml file:\n")
    print("-" * 50)
    print(f'gdrive_folder_id = "YOUR_FOLDER_ID_HERE"')
    print("")
    print("[oauth_info]")
    print(f'token = "{creds.token}"')
    print(f'refresh_token = "{creds.refresh_token}"')
    print(f'token_uri = "{creds.token_uri}"')
    print(f'client_id = "{creds.client_id}"')
    print(f'client_secret = "{creds.client_secret}"')
    print(f'scopes = {json.dumps(creds.scopes)}')
    print("-" * 50)

if __name__ == '__main__':
    main()

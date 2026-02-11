import streamlit as st
import os
import toml
from google.oauth2 import service_account
from googleapiclient.discovery import build

def check_drive_access():
    try:
        # Load secrets
        secrets_path = ".streamlit/secrets.toml"
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
        else:
            print(f"Error: {secrets_path} not found.")
            return

        if "gcp_service_account" not in secrets:
            print("Error: 'gcp_service_account' not found in secrets.")
            return

        service_account_info = secrets["gcp_service_account"]
        
        # Scope for Drive API (using readonly scope to test visibility)
        SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        
        creds = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)
        
        service = build('drive', 'v3', credentials=creds)

        print(f"Authenticated as: {service_account_info.get('client_email')}")
        
        # List first 10 files/folders
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print("No files or folders found accessible to this service account.")
            print("Please share your target folder with the service account email.")
        else:
            print("Files/Folders accessible:")
            for item in items:
                print(f"{item['name']} ({item['id']}) - {item['mimeType']}")
                
        # Check specific folder ID
        target_folder_id = secrets.get("gdrive_folder_id")
        if target_folder_id:
            try:
                folder = service.files().get(fileId=target_folder_id, fields="id, name").execute()
                print(f"\nSUCCESS! Found target folder: {folder['name']} ({folder['id']})")
            except Exception as e:
                print(f"\nFAILURE! Could not find target folder ID: {target_folder_id}")
                print(f"Error details: {e}")
                print("\nDouble check that you have shared this folder with the service account email above!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_drive_access()

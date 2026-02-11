import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import json

# Page Configuration
st.set_page_config(page_title="Remote Code Bridge", page_icon="🌉", layout="centered")

# --- Password Protection ---
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets.get("app_password", "admin"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()  # Stop execution if password not correct
# ---------------------------

st.title("🌉 Remote Code Bridge")
st.markdown("Bridge your code from **Restriction** to **Freedom**.")

# 1. Inputs
col1, col2 = st.columns([3, 1])
with col1:
    filename = st.text_input("Filename (without extension)", placeholder="e.g., my_script")
with col2:
    extension = st.selectbox("Extension", [".py", ".md", ".txt", ".csv", ".json"])

content = st.text_area("File Content", height=300, placeholder="Paste your code or text here...")

# 2. Google Drive Authentication & Upload
def upload_to_drive(filename, content, extension):
    try:
        # Load secrets
        if "oauth_info" not in st.secrets:
            st.error("Secrets not found! Please configure .streamlit/secrets.toml with [oauth_info]")
            return False

        oauth_info = st.secrets["oauth_info"]
        
        # Create Credentials object from secrets
        creds = Credentials(
            token=oauth_info["token"],
            refresh_token=oauth_info["refresh_token"],
            token_uri=oauth_info["token_uri"],
            client_id=oauth_info["client_id"],
            client_secret=oauth_info["client_secret"],
            scopes=json.loads(oauth_info["scopes"]) if isinstance(oauth_info["scopes"], str) else oauth_info["scopes"]
        )
        
        service = build('drive', 'v3', credentials=creds)
        
        # Target Folder ID
        folder_id = st.secrets.get("gdrive_folder_id")
        if not folder_id:
             st.error("Google Drive Folder ID not found in secrets!")
             return False

        full_filename = f"{filename}{extension}"
        
        # Create file metadata
        file_metadata = {
            'name': full_filename,
            'parents': [folder_id]
        }
        
        # Create media
        media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8')), mimetype='text/plain')
        
        # Execute upload
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        return file.get('id')

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# 3. Action
if st.button("🚀 Send to Home", type="primary"):
    if not filename:
        st.warning("Please enter a filename.")
    elif not content:
        st.warning("Please enter some content.")
    else:
        with st.spinner("Bridging data..."):
            file_id = upload_to_drive(filename, content, extension)
            if file_id:
                st.success(f"Success! File '{filename}{extension}' uploaded (ID: {file_id})")
                st.balloons()

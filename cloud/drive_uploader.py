import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate using credentials/creds.json
gauth = GoogleAuth()
gauth.LoadCredentialsFile("credentials/creds.json")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("credentials/creds.json")
drive = GoogleDrive(gauth)

# Shared Google Drive folder ID
FOLDER_ID = '1VlB7gqES85fusrjaIOpd5G0SAxB57UUz'


def upload_snapshot(file_path):
    """
    Uploads a local image file to Google Drive and returns its public URL.
    """
    try:
        file_name = os.path.basename(file_path)
        gfile = drive.CreateFile({'parents': [{'id': FOLDER_ID}], 'title': file_name})
        gfile.SetContentFile(file_path)
        gfile.Upload()
        gfile.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        file_url = f"https://drive.google.com/uc?id={gfile['id']}"
        print(f"[UPLOAD] Snapshot uploaded: {file_url}")
        return file_url
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return ""

import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

FILE_ID = os.environ["HTML_FILE_ID"]
DEST_DIR = "public"
DEST_FILE = os.path.join(DEST_DIR, "index.html")

os.makedirs(DEST_DIR, exist_ok=True)

creds = service_account.Credentials.from_service_account_info(
    eval(os.environ["GCP_SA_KEY"]),
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

drive = build("drive", "v3", credentials=creds)

request = drive.files().get_media(fileId=FILE_ID)
fh = io.FileIO(DEST_FILE, "wb")
downloader = MediaIoBaseDownload(fh, request)

done = False
while not done:
    status, done = downloader.next_chunk()
    print(f"Downloading... {int(status.progress() * 100)}%")

print("✅ File downloaded to public/index.html")

import os
import io
import random
import string
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

FILE_ID = os.environ["HTML_FILE_ID"]
DEST_DIR = "output_files"

# ✅ Generate a random 16-character key
random_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
file_name = f"{random_key}.html"
file_path = os.path.join(DEST_DIR, file_name)

# ✅ Ensure output_files/ directory exists
os.makedirs(DEST_DIR, exist_ok=True)

# ✅ Authenticate with service account
creds = service_account.Credentials.from_service_account_info(
    eval(os.environ["GCP_SA_KEY"]),
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

drive = build("drive", "v3", credentials=creds)

# ✅ Download the file
request = drive.files().get_media(fileId=FILE_ID)
fh = io.FileIO(file_path, "wb")
downloader = MediaIoBaseDownload(fh, request)

done = False
while not done:
    status, done = downloader.next_chunk()
    print(f"⬇️ Downloading... {int(status.progress() * 100)}%")

print(f"✅ Dashboard saved as {file_path}")

# ✅ Save the generated key so GitHub Actions can access it
with open("dashboard_key.txt", "w") as f:
    f.write(random_key)

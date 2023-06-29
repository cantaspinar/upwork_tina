import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from config import service_account_path


credentials = service_account.Credentials.from_service_account_file(
    service_account_path)
scope = ['https://www.googleapis.com/auth/drive.readonly']
credentials = credentials.with_scopes(scope)

service = build('drive', 'v3', credentials=credentials)


def list_files(folder_id):
    results = service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                   fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def download_file(file_id, file_name, download_path):

    request = service.files().get_media(fileId=file_id)

    # Create the download directory if it doesn't exist
    os.makedirs(download_path, exist_ok=True)

    file_path = os.path.join(download_path, file_name)

    if os.path.exists(file_path):
        print(
            f"File '{file_name}' already exists in the '{download_path}' folder.")
        return

    with open(file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

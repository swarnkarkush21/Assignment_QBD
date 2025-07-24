# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 13:48:19 2025

@author: Kush Swarnkar
"""
from googleapiclient.discovery import build
from google.oauth2 import service_account
# If using OAuth for user credentials (less common for server-side)
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
import os
import io
from googleapiclient.http import MediaIoBaseDownload
from config import GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY_PATH, GOOGLE_DRIVE_SCOPES

class DriveConnector:
    def __init__(self):
        self.creds = None
        self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)

    def _authenticate(self):
        # Authenticate using a service account (recommended for server-side applications)
        # You would download a JSON key file for your service account from the Google Cloud Console.
        if os.path.exists(GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY_PATH):
            self.creds = service_account.Credentials.from_service_account_file(
                GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY_PATH, scopes=GOOGLE_DRIVE_SCOPES
            )
        else:
            raise FileNotFoundError(f"Google Drive service account key not found at {GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY_PATH}")
        # For OAuth flow (desktop app example, if needed):
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     GOOGLE_DRIVE_CLIENT_SECRETS_PATH, GOOGLE_DRIVE_SCOPES
        # )
        # self.creds = flow.run_local_server(port=0)

    def list_files(self):
        # Fetch file metadata, including name, id, and webViewLink (for HTTP URL).
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name, mimeType, webViewLink)"
        ).execute()
        items = results.get('files', [])
        return items

    def download_file(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        file_path = f"temp_{file_name}"  # Temporary file name for local storage
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file_path
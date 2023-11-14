import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import json
import logging

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None

    json_file = f'./keys/token_{API_SERVICE_NAME}_{API_VERSION}.json'

    if os.path.exists(json_file):
        with open(json_file, 'r') as token:
            cred_data = json.load(token)
            cred = Credentials.from_authorized_user_info(cred_data)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        # Save credentials to the JSON file
        cred_data = {
            'token': cred.token,
            'refresh_token': cred.refresh_token,
            'token_uri': cred.token_uri,
            'client_id': cred.client_id,
            'client_secret': cred.client_secret,
            'scopes': cred.scopes
        }
        with open(json_file, 'w') as token:
            json.dump(cred_data, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred,static_discovery=False)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
    
    print(cred_data)
    print(f"is valid : {cred.valid}")
    return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


def sync_photos(service):
    # Retrieve the list of media items (photos) from Google Photos
    results = service.mediaItems().list().execute()
    items = results.get("mediaItems", [])

    if not items:
        print("No media items found.")
    else:
        print("Media items:")
        for item in items:
            filename = item["filename"]
            print(filename)
            # You can save this filename to the SQLite database or perform other actions.

            
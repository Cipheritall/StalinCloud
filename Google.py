import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import json
import logging
from download import download_file,download_photo,download_video
import db
from config import CONFIG

API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = './keys/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']

def Create_Service():
    cred = None
    json_file = f'./keys/token_{API_SERVICE_NAME}_{API_VERSION}.json'
    logging.info(f"Using token {json_file}")
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
        logging.info(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
    
    logging.info(f"cred_data validity : {cred.valid}")
    return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

def photos_round(service,pageSize=25,token=None):
    added = 0
    if token==None:
        results = service.mediaItems().list(pageSize=pageSize).execute()
    else:
        results = service.mediaItems().list(pageSize=pageSize, pageToken=token).execute()
    next_page_token = results['nextPageToken']
    items = results.get("mediaItems", [])
    if not items:
        print("No media items found.")
        return None,None
    else:
        print("Media items:")
        for item in items:
            gid = item["id"]
            is_in_db = db.is_photo_in_db(gid)
            is_downloaded =  db.is_photo_downloaded(gid)
            if not is_downloaded:
                filename = item["filename"]
                # You can save this filename to the SQLite database or perform other actions.
                # add to db
                item["owner"]=CONFIG["owner"]
                try:
                    if not is_in_db:
                        db.add_new_photo(item)
                    file_path = CONFIG["media_path"]+"/"+filename
                    if item['mimeType'].find("image")>-1:
                        download_photo(item["baseUrl"], file_path)
                    elif item['mimeType'].find("video")>-1:
                        download_video(item["baseUrl"], file_path)
                    else:
                        download_file(item["baseUrl"], file_path)
                    db.mark_as_downloaded(gid,file_path)
                    added+=1
                    # delete from google cloud
                except Exception as e:
                    logging.error(e)
        return "Done",next_page_token,added
 
def sync_photos(service,target_num=55,batch=25):
    index = 0
    # Retrieve the list of media items (photos) from Google Photos
    status,token,added = photos_round(service,pageSize=batch)
    if status == "Done":
        index+=added
    while index < target_num :
        status,token,added = photos_round(service,pageSize=batch,token=token)
        index+=added
    return
                
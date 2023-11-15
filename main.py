import os
from Google import Create_Service,sync_photos
import logging
import db
from config import CONFIG
logging.basicConfig(filename="log/main.log", level=logging.DEBUG)

API_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = './keys/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']

db.create_database(CONFIG["db"])
service = Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES)
sync_photos(service)
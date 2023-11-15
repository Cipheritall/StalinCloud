import os
from Google import Create_Service,sync_photos
import logging
import db
from config import CONFIG
logging.basicConfig(filename="log/main.log", level=logging.DEBUG)


db.create_photos_database()
service = Create_Service()
sync_photos(service,target_num=100)
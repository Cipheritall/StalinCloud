import files
import db 
import logging 
from config import CONFIG

logger = logging.getLogger(__name__)

def move_photo(google_id,new_path):
    photo_info = db.get_photo_by_google_id(google_id)
    local_path = photo_info["local_path"]
    if files.file_exists(local_path):
        files.move_file(local_path, new_path)
        if files.file_exists(new_path):
            db.update_photo_path(google_id, new_path)

def move_all_photos():
    photos = db.get_all_photos()
    if photos:
        logger.info("All photos in the database:")
        for photo in photos:
            old_path = photo["local_path"]
            if old_path == None:
                continue 
            files.create_folder_if_not_exist(CONFIG["media_path"])
            new_path = CONFIG["media_path"]+"/"+old_path.split("/")[-1]
            google_id =  photo["google_id"]
            logger.info(f"Moving from {old_path} to {new_path} : {google_id}")
            move_photo(google_id,new_path)
    else:
        print("No photos found in the database.")    
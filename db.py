import sqlite3
import datetime
import logging
from config import CONFIG


# Configure the logging module
logger = logging.getLogger(__name__)

DATABASE_FILE = CONFIG["db"]
def create_photos_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                google_id TEXT,
                album TEXT,
                owner TEXT,
                filename TEXT,
                created_time TEXT,
                downloaded_time TEXT,
                local_path TEXT,
                productUrl TEXT,
                baseUrl TEXT,
                mimeType TEXT
            )
            """
        )
        conn.commit()
        conn.close()
        logger.info("Database created successfully.")
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")

def add_new_photo(photo_info):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO photos (
                    google_id, album, owner, filename, created_time,
                    downloaded_time, local_path, productUrl, baseUrl, mimeType
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                photo_info.get("id", None),
                photo_info.get("album", None),
                photo_info.get("owner", None),
                photo_info.get("filename", None),
                photo_info["mediaMetadata"].get("creationTime", None),
                photo_info.get("downloaded_time", None),
                photo_info.get("local_path", None),
                photo_info.get("productUrl", None),
                photo_info.get("baseUrl", None),
                photo_info.get("mimeType", None),
            ))
            conn.commit()
            logger.info(f"Photo added successfully {photo_info['id']}.")
    except Exception as e:
        logger.error(f"Error adding photo to the database: {str(e)}")


def get_all_photos():
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Retrieve all photo records from the database
        cursor.execute("SELECT * FROM photos")
        results = cursor.fetchall()

        conn.close()

        photo_list = []
        for result in results:
            photo_info = {
                "id": result[0],
                "google_id": result[1],
                "album": result[2],
                "owner": result[3],
                "filename": result[4],
                "created_time": result[5],
                "downloaded_time": result[6],
                "local_path": result[7],
                "productUrl": result[8],
                "baseUrl": result[9],
                "mimeType": result[10],
            }
            photo_list.append(photo_info)
        return photo_list
    except Exception as e:
        logger.error(f"Error getting photos from database: {str(e)}")
        return None

def get_photo_by_google_id(google_id):
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Retrieve photo information from the database based on the google_id
        cursor.execute(
            "SELECT * FROM photos WHERE google_id = ?",
            (google_id,)
        )
        result = cursor.fetchone()

        conn.close()

        if result:
            # Convert the result to a dictionary for easier use
            photo_info = {
                "id": result[0],
                "google_id": result[1],
                "album": result[2],
                "owner": result[3],
                "filename": result[4],
                "created_time": result[5],
                "downloaded_time": result[6],
                "local_path": result[7],
                "productUrl": result[8],
                "baseUrl": result[9],
                "mimeType": result[10],
            }
            return photo_info
        else:
            logger.warning(f"No photo found with Google ID {google_id}")
            return None

    except Exception as e:
        logger.error(f"Error getting photo from database: {str(e)}")
        return None

def update_photo_path(google_id, new_local_path):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Update the local_path field for the given photo_id
        cursor.execute(
            """
            UPDATE photos
            SET local_path = ?
            WHERE google_id = ?
            """,
            (new_local_path, google_id)
        )

        conn.commit()
        conn.close()
        logger.info(f"Updated local path for photo with id {google_id}")
    except Exception as e:
        logger.error(f"Error updating photo path: {str(e)}")

def is_photo_in_db(google_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM photos WHERE google_id = ?', (google_id,))
            return cursor.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"Error checking if photo is in the database: {str(e)}")
        return False

def is_photo_downloaded(google_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM photos WHERE google_id = ? AND downloaded_time IS NOT NULL', (google_id,))
            return cursor.fetchone()[0] > 0
    except Exception as e:
        logger.error(f"Error checking if photo is downloaded: {str(e)}")
        return False

def mark_as_downloaded(google_id, local_path):
    try:
        downloaded_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE photos
                SET downloaded_time = ?, local_path = ?
                WHERE google_id = ?
            ''', (downloaded_time, local_path, google_id))
            conn.commit()
            logger.info(f"Photo marked as downloaded successfully {google_id}.")
    except Exception as e:
        logger.error(f"Error marking photo as downloaded: {str(e)}")

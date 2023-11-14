import sqlite3
from config import CONFIG
import datetime

DATABASE_FILE = "./db/photos.db"

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id TEXT PRIMARY KEY AUTOINCREMENT,
            google_id TEXT,
            album TEXT,
            owner TEXT,
            filename TEXT,
            created_time TEXT,
            downloaded_time TEXT,
            local_path TEXT,
            productUrl TEXT,
            baseUrl TEXT,
            mimeType TEXT,
        )
        """
    )
    conn.commit()
    conn.close()


def add_new_photo(photo_info):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO photos (
                google_id, album, owner, filename, created_time,
                downloaded_time, local_path, productUrl, baseUrl, mimeType
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            photo_info.get("google_id", None),
            photo_info.get("album", None),
            photo_info.get("owner", None),
            photo_info.get("filename", None),
            photo_info.get("created_time", None),
            photo_info.get("downloaded_time", None),
            photo_info.get("local_path", None),
            photo_info.get("productUrl", None),
            photo_info.get("baseUrl", None),
            photo_info.get("mimeType", None),
        ))
        conn.commit()

def is_photo_in_db(google_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM photos WHERE google_id = ?', (google_id,))
        return cursor.fetchone()[0] > 0

def is_photo_downloaded(google_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM photos WHERE google_id = ? AND downloaded_time IS NOT NULL', (google_id,))
        return cursor.fetchone()[0] > 0

def mark_as_downloaded(google_id, local_path):
    downloaded_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE photos
            SET downloaded_time = ?, local_path = ?
            WHERE google_id = ?
        ''', (downloaded_time, local_path, google_id))
        conn.commit()
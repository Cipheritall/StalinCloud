import sqlite3
from config import CONFIG

DATABASE_FILE = "./db/photos.db"

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id TEXT PRIMARY KEY,
            owner TEXT,
            filename TEXT,
            created_time TEXT,
            downloaded_time TEXT,
            download_url TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def add_new_photo(photo_info):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO photos (id, owner, filename, created_time, downloaded_time, download_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            photo_info["id"],
            CONFIG['owner'],
            photo_info["filename"],
            photo_info["created_time"],
            photo_info.get("downloaded_time", None),
            photo_info["download_url"],
        ))
        conn.commit()

def is_photo_in_db(photo_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM photos WHERE id = ?', (photo_id,))
        return cursor.fetchone()[0] > 0

def is_photo_downloaded(photo_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM photos WHERE id = ? AND downloaded_time IS NOT NULL', (photo_id,))
        return cursor.fetchone()[0] > 0

def mark_as_downloaded(photo_id, downloaded_time):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE photos
            SET downloaded_time = ?
            WHERE id = ?
        ''', (downloaded_time, photo_id))
        conn.commit()
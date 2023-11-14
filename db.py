import sqlite3

DATABASE_FILE = "./db/photos.db"

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id TEXT PRIMARY KEY,
            filename TEXT,
            created_time TEXT,
            downloaded_time TEXT,
            download_url TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def save_to_database(photo_info):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO photos (id, filename, created_time, download_url)
        VALUES (?, ?, ?, ?)
        """,
        (
            photo_info["id"],
            photo_info["filename"],
            photo_info["created_time"],
            photo_info["download_url"],
        ),
    )
    conn.commit()
    conn.close()

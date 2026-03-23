import sqlite3

DB_NAME = "multimodal.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        image_data BLOB,
        caption TEXT,
        ocr_text TEXT,
        features TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def insert_data(image_name, image_data, caption, ocr_text, features):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO images (image_name, image_data, caption, ocr_text, features)
    VALUES (?, ?, ?, ?, ?)
    """, (image_name, image_data, caption, ocr_text, features))

    conn.commit()
    conn.close()

def get_all_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT image_data, caption, ocr_text FROM images ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows

def search_data(query):
    conn = connect_db()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT image_data, caption, ocr_text 
    FROM images
    WHERE caption LIKE ? OR ocr_text LIKE ?
    ORDER BY id DESC
    """, (f"%{query}%", f"%{query}%"))

    rows = cursor.fetchall()
    conn.close()
    return rows

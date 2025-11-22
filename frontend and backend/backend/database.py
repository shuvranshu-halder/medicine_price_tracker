import sqlite3

DB_NAME = "medicines.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            count INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

def save_search(medicine_name):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM searches WHERE name = ?", (medicine_name,))
    row = cursor.fetchone()

    if row:
        # update existing
        cursor.execute("UPDATE searches SET count = count + 1 WHERE name = ?", (medicine_name,))
    else:
        # insert new
        cursor.execute("INSERT INTO searches (name, count) VALUES (?, ?)", (medicine_name, 1))

    conn.commit()
    conn.close()

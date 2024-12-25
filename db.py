import sqlite3

# Path to the SQLite database
DATABASE_PATH = "./databases/mental_health.db"

def create_table():
    """
    Creates the mental_health table in the SQLite database if it doesn't exist.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mental_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                feeling INTEGER,
                serenity INTEGER,
                sleep INTEGER,
                productivity INTEGER,
                enjoyment INTEGER,
                average REAL
            )
        ''')

def add_entry(date, feeling, serenity, sleep, productivity, enjoyment, average):
    """
    Inserts a new entry into the mental_health table.

    Args:
        date (str): The date of the entry.
        feeling (int): Feeling score (0-10).
        serenity (int): Serenity score (0-10).
        sleep (int): Sleep score (0-10).
        productivity (int): Productivity score (0-10).
        enjoyment (int): Enjoyment score (0-10).
        average (float): Average score of the above.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mental_health (date, feeling, serenity, sleep, productivity, enjoyment, average)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, feeling, serenity, sleep, productivity, enjoyment, average))
        conn.commit()

def fetch_all():
    """
    Fetches all entries from the mental_health table.

    Returns:
        list: A list of all rows in the table.
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mental_health")
        return cursor.fetchall()

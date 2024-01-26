import sqlite3

def create_table():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_ (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        country_article TEXT,
        searches INTEGER
    );
    """

    try:
        cursor.execute(create_table_query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        cursor.close()
        conn.close()

# Вы можете вызвать эту функцию перед основной функцией main
if __name__ == "__main__":
    create_table()

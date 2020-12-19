import sqlite3

const = 0


def create_connection():
    conn = sqlite3.connect('users.db')  # записать в отдельный файл
    cur = conn.cursor()
    return cur, conn


def create_users(cur, conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user INTEGER PRIMARY KEY,
        user_id   TEXT,   
        steam_link TEXT);
        """)
    conn.commit()
    pass


def users_table_output(cur):
    cur.execute("SELECT * FROM users;")
    one_result = cur.fetchone()
    print(one_result)
    pass


def users_add(cur, conn, user_id, link):
    global const
    const += 1
    cur.execute("INSERT INTO text_index VALUES (?,?,?)", (const, user_id, link))
    conn.commit()
    pass


'''connection = sqlite3.connect('games')
cur2 = connection.cursor()

connection.execute("""
    CREATE TABLE IF NOT EXISTS users(
    game_id INTEGER PRIMARY KEY,
    game_name TEXT,
    discount INTEGER,
    COUNT INTEGER);
    """)
connection.commit()'''

if __name__ == "__main__":
    create_connection()

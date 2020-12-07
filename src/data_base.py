import sqlite3

conn = sqlite3.connect('users.db')  #записать в отдельный файл
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    steam_link TEXT);
    """)
conn.commit()

cur.execute("SELECT * FROM users;")
one_result = cur.fetchone()
print(one_result)

connection = sqlite3.connect('games')
cur2 = connection.cursor()

connection.execute("""
    CREATE TABLE IF NOT EXISTS users(
    game_id INTEGER PRIMARY KEY,
    game_name TEXT,
    discount INTEGER,
    COUNT INTEGER);
    """)
connection.commit()
import sqlite3

conn = sqlite3.connect('tier_list.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS element (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  group TEXT,
                  source TEXT,
                  category_id INTEGER NULLABLE,
                  order INTEGER NULLABLE,
                  FOREIGN KEY (category_id) REFERENCES category(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT)''')

conn.commit()
conn.close()
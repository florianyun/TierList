import sqlite3

conn = sqlite3.connect('tier_list.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS element (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  titre TEXT,
                  groupe TEXT,
                  source TEXT,
                  categorie_id INTEGER NULLABLE,
                  ordre INTEGER NULLABLE,
                  FOREIGN KEY (categorie_id) REFERENCES categorie(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS categorie (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nom TEXT)''')

conn.commit()
conn.close()
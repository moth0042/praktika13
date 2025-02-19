import sqlite3 as sq

con = sq.connect('my_database.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER)''')

cur.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')




con.commit()
con.close()

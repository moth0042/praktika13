import sqlite3 as sq

con = sq.connect('my_database.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER)''')





con.commit()
con.close()

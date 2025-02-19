import sqlite3 as sq

con = sq.connect('my_database.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER)''')

cur.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')

cur.execute('''INSERT INTO Users (username, email, age) VALUES ('newuser', 'newuser@example.com', 28)''')

cur.execute('''UPDATE Users SET age = 29 WHERE username = "newuser"''')





con.commit()
con.close()

cur.execute('SELECT * FROM Users')
users = cur.fetchall()
for user in users:
    print(user)

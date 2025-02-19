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

cur.execute('''DELETE FROM Users WHERE username = "newuser"''')
cur.execute('''DELETE FROM Users''')

cur.execute('''INSERT INTO Users (username, email, age) VALUES ('newuser', 'newuser@example.com', 28)''')
cur.execute('''INSERT INTO Users (username, email, age) VALUES ('newuser2', 'newuser2@example.com', 24)''')
cur.execute('''INSERT INTO Users (username, email, age) VALUES ('newuser3', 'newuser3@example.com', 19)''')
cur.execute('''INSERT INTO Users (username, email, age) VALUES ('moth0042', 'moth0042@example.com', 42)''')
cur.execute('''INSERT INTO Users (username, email, age) VALUES ('aerty', 'aerty@example.com', 22)''')
cur.execute('''INSERT INTO Users (username, email, age) VALUES ('user45', 'usr4555@example.com', 33)''')

cur.execute('SELECT * FROM Users')
users = cur.fetchall()
for user in users:
    print(user)

cur.execute('SELECT username, age FROM Users WHERE age > 25')
users = cur.fetchall()
for user in users:
    print(user)

cur.execute('SELECT age, AVG(age) as average_age FROM Users GROUP BY age')
users = cur.fetchall()
for user in users:
    print(user)

cur.execute('SELECT age, AVG(age) as average_age FROM Users GROUP BY age HAVING AVG(age) > 30')
users = cur.fetchall()
for user in users:
    print(user)

cur.execute('SELECT username, age FROM Users ORDER BY age DESC')
users = cur.fetchall()
for user in users:
    print(user)

cur.execute('SELECT age, AVG(age) as average_age FROM Users GROUP BY age HAVING AVG(age) > 30 ORDER BY age DESC')
users = cur.fetchall()
for user in users:
    print(user)


cur.execute('SELECT COUNT(*) FROM Users')
n = cur.fetchone()[0]
print('users count: ', n)

cur.execute('SELECT SUM(age) FROM Users')
n = cur.fetchone()[0]
print('users ages sum : ', n)

cur.execute('SELECT AVG(age) FROM Users')
n = cur.fetchone()[0]
print('average user age: ', n)

cur.execute('SELECT MIN(age) FROM Users')
n = cur.fetchone()[0]
print('min user age: ', n)

cur.execute('SELECT MAX(age) FROM Users')
n = cur.fetchone()[0]
print('max user age: ', n)


cur.execute('SELECT username, age FROM Users WHERE age = (SELECT MAX(age) FROM Users)')
users = cur.fetchall()
for user in users:
    print(user)

con.commit()
con.close()



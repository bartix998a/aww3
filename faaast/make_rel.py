import sqlite3

db = sqlite3.connect('fast.db')
cur = db.cursor()
print(cur.execute('SELECT * FROM image').fetchall())
print(cur.execute('SELECT * FROM img_tag').fetchall())
print(cur.execute('SELECT * FROM tag').fetchall())
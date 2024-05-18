import sqlite3

db = sqlite3.connect('fast.db')
cur = db.cursor()
cur.execute("DELETE from image")
cur.execute("DELETE FROM tag")
cur.execute("DELETE from img_tag")
db.commit()
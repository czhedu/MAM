import uuid
import sqlite3

con = sqlite3.connect('temp.db3')
cur = con.cursor()
uuid_str = str(uuid.uuid4())

sql = 'INSERT INTO word_image (uuid, word, image) VALUES("%s", "%s", "%s")' % \
      (uuid_str, "word", "image")

cur.execute(sql) 
#cur.execute('INSERT INTO word_image (uuid, word, image) VALUES("word", "image")')
con.commit()



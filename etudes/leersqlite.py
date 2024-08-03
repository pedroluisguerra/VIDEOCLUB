import sqlite3


con = sqlite3.connect("data\peliculas.sqlite")
cur = con.cursor()
cur.execute("SELECT id, nombre, url_foto, url_web FROM directores")
result = cur.fetchall()

print(result)  # You can process the row here

con.close()


import sqlite3

con = sqlite3.connect("data\peliculas.sqlite")
cur = con.cursor()

nombre = input("Nombre:")
foto = input("url foto: ")
web = input ("url web: ")

query = "INSERT INTO directores (nombre, url_foto, url_web) VALUES (?, ?, ?)"
print(query)
cur.execute(query, (nombre, foto, web))
con.commit()
    

con.close()
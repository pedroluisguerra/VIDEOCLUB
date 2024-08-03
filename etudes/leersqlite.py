import sqlite3

# Abrir conexión
con = sqlite3.connect("data\peliculas.sqlite")

# Crear cursor
cur = con.cursor()


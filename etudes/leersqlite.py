import sqlite3, itertools

def rows_to_dictlist(rows, names):
    # Extraer los nombres de las columnas
    column_names = [col[0] for col in names]

    # Crear diccionarios usando itertools.starmap
    result_dicts = list(itertools.starmap(lambda *args: dict(zip(column_names, args)), rows))
    return result_dicts


# Abrir conexión 
con = sqlite3.connect("data\peliculas.sqlite")

# Crear cursor
cur = con.cursor()

# Uso el cursor con SQL en forma de cadena
cur.execute("SELECT id, nombre, url_foto, url_web FROM directores")

columns_description = cur.description

# Proceso al respuesta si la hubiera  (un select)
result = cur.fetchall()

# Hacer una función que em transforme la lista de tuplas result en una lista de diccionario como  la que devuelve el dict reader
# print(columns_description)  # You can process the row here

'''
# Extraer los nombres de las columnas
column_name = [col[0] for col in columns_description]

# Crear la lista de diccionarios
dicts_lists = []
for row in result:
    row_dict = {}
    for i, value in enumerate(row):
        row_dict[column_name[i]] = value
    dicts_lists.append(row_dict)

# Imprimir el resultado
for item in dicts_lists:
    print(item)
'''
resultado = rows_to_dictlist(result, columns_description)

print(resultado)

con.close()


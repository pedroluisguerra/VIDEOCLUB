fichero = open("data/generos.csv", "r")
print(fichero.read(8))
print(fichero.read(8))
print(fichero.readline())
print(fichero.readline())
print(fichero.readline())
for linea in fichero:
    print(linea)
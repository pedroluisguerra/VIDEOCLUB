from abc import ABC, abstractmethod
import csv
import sqlite3
import itertools
import os

class Model(ABC):
    @classmethod
    @abstractmethod
    def create_from_dict(cls, diccionario):
        pass

class Director(Model):

    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["nombre"],int(diccionario["id"]))
    
    def __init__(self, nombre: str, id: int = -1):
        self.nombre = nombre
        self.id = id

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):                        
            return self.id == other.id and self.nombre == other.nombre
        return False
    
    def __hash__(self) -> int:
        return hash(self.id, self.nombre)

    def __repr__(self) -> str:
        return f"Director ({self.id}): {self.nombre}"    
    
class Pelicula(Model):

    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(diccionario["titulo"], 
                   diccionario["sinopsis"], 
                   int(diccionario["director_id"]), 
                   int(diccionario["id"]))
    
    def __init__(self, titulo: str, sinopsis: str, director: object, id: int = -1):
        self.titulo = titulo
        self.sinopsis = sinopsis
        self.id = id
        self.director = director       

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, value):
         
        if isinstance(value, Director):
            self._director = value
            self._id_director = value.id
        elif isinstance(value, int):
            self._director = None
            self._id_director = value
        else:
            raise TypeError(F"{value} debe ser entero o instancia de Director")
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):                        
            return self.titulo == other.titulo and self.sinopsis == other.sinopsis and self.director == other.director and self.id == other.id
        return False
    
    def __hash__(self) -> int:
        return hash((self.titulo, self.sinopsis, self._director, self.id))

    def __repr__(self) -> str:
        return f"Pelicula ({self.titulo}): {self.sinopsis}, {self._director}, {self.id}"
   
class Genero(Model):

    @classmethod
    def create_from_dict(cls, diccionario):
        return cls(int(diccionario["id"]), diccionario["genero"])
    
    def __init__(self, name: str, id: int = -1):
        self.name = name
        self.id = id

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):                        
            return self.id == other.id and self.name == other.name
        return False
    
    def __hash__(self) -> int:
        return hash(self.id, self.name)

    def __repr__(self) -> str:
        return f"Genero ({self.id}): {self.name}"     

class DAO(ABC):

    """
    @abstractmethod
    def guardar(self, instancia):
        pass

    @abstractmethod
    def actualizar(self, instancia):
        pass
    
    @abstractmethod
    def borrar(self, instancia):
        pass

    @abstractmethod
    def consultar(self, instancia):
        pass
    """
    @abstractmethod
    def todos(self):
        pass

class DAO_CSV(DAO):    
    model = None

    def __init__(self, path, encoding = "utf-8"):
        self.path = path
        self.encoding = encoding

    def todos(self):
        with open(self.path, "r", newline="", encoding = self.encoding) as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")
            lista = []
            for registro in lector_csv:
                lista.append(self.model.create_from_dict(registro))
        return lista

class DAO_CSV_Director(DAO_CSV):

    model = Director

class DAO_CSV_Pelicula(DAO_CSV):
   
    model = Pelicula

class DAO_CSV_Genero(DAO_CSV):
   
    model = Genero

class DAO_SQLite(DAO):
    model = None
    table = None
    

    def __init__(self, path) -> None:
        self.path = path

    def todos(self):
        
        '''
        acceder a sqlite y traer todos los registros de la table del modelo con la función rows_to_dictlist traerlos en forma de diccionario
        '''
        print(f"Ruta de la base de datos: {self.path}")
        conn = sqlite3.connect(self.path)

        cur = conn.cursor()

        cur.execute(f"select * from {self.table}")

        lista = self.__rows_to_dictlist(cur.fetchall(),cur.description)
        
        conn.close()

        return lista

    def __rows_to_dictlist(self, rows, names):
       # Extraer los nombres de las columnas
       column_names = [col[0] for col in names]

       # Crear diccionarios usando itertools.starmap
       lists_dicts = list(itertools.starmap(lambda *args: dict(zip(column_names, args)), rows))
       
       # Convertir diccionarios en instancias del modelo usando map
       resultado = list(map(self.model.create_from_dict, lists_dicts))

       return resultado   

class DAO_SQLite_Director(DAO_SQLite):
    model = Director
    table = "directores"
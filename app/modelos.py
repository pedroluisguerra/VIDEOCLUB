from abc import ABC, abstractmethod
import csv

class Director:
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
    
class Pelicula:
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

class DAO_CSV_Director(DAO):

    def __init__(self, path):
        self.path = path

    def todos(self):
        with open(self.path, "r", newline="") as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")
            
            lista_directores = []
            for registro in lector_csv:
                lista_directores.append(Director(registro["nombre"],int(registro["id"])))
        
        return lista_directores

class DAO_CSV_Pelicula(DAO):
    def __init__(self, path: str):
        self.path = path

    def todos(self):
        with open(self.path, "r", newline="") as fichero:
            lector_csv = csv.DictReader(fichero, delimiter=";", quotechar="'")
            lista = []
            for registro in lector_csv:
                lista.append(Pelicula(registro["titulo"], 
                                      registro["sinopsis"], 
                                      int(registro["director_id"]), 
                                      int(registro["id"])))
                
        return lista
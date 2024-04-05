
#JIA YI HE

class Animal:
    def __init__(self, especie, sonido):
        self._especie = especie  
        self._sonido = sonido

    def hacer_sonido(self):
        print(f"{self._especie} hace el sonido: {self._sonido}")

class Gato(Animal):
    def __init__(self, nombre, color):
        super().__init__("Gato", "Miau") 
        self._nombre = nombre
        self._color = color

    def hacer_sonido(self):
        super().hacer_sonido()
        print(f"{self._nombre} es un gato de color {self._color}.")

from abc import ABC, abstractmethod

class Hábitat(ABC):
    abstractmethod
    def descripcion(self):
        pass

class Bosque(Hábitat):
    def descripcion(self):
        return "Un hábitat con un crecimiento denso de árboles y vegetación."

def describir_hábitat(hábitat):
    return hábitat.descripcion()

bosque = Bosque()
print(f"Descripción del Hábitat: {describir_hábitat(bosque)}")

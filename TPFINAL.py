import math
import random
from abc import ABC, abstractmethod

class Vehiculos:

    def __init__(self, nombre, velocidad, capacidad, costofijo, costoporkm, costoporkg):
        self.nombre = nombre
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costofijo = costofijo
        self.costoporkm = costoporkm
        self.costoporkg = costoporkg

    def get_nombre(self):
        return self.get_nombre()

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_velocidad(self):
        return self.get_velocidad()

    def get_capacidad(self):
        return self.get_capacidad()

    def get_costofijo(self):
        return self.get_costofijo()

    def get_costoporkm(self):
        return self.get_costoporkm()

    def get_costoporkg(self):
        return self.get_costoporkg()

    def set_velocidad(self, velocidad):
        self.velocidad = velocidad

    def set_capacidad(self, capacidad):
        self.capacidad = capacidad

    def set_costofijo(self, costofijo):
        self.costofijo = costofijo

    def set_costoporkm(self, costoporkm):
        self.costoporkm = costoporkm

    def set_costoporkg(self, costoporkg):
        self.costoporkg = costoporkg

    @abstractmethod
    def calcular_costo(self, distancia, carga):
        pass

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_velocidad(self):
        return self.velocidad

    def set_velocidad(self, velocidad):
        self.velocidad = velocidad

    def get_costofijo(self):
        return self.costofijo

    def set_costofijo(self, costofijo):
        self.costofijo = costofijo

    def get_costoporkm(self):
        return self.costoporkm

    def set_costoporkm(self, costoporkm):
        self.costoporkm = costoporkm

    def get_costoporkg(self):
        return self.costoporkg

    def set_costoporkg(self, costoporkg):
        self.costoporkg = costoporkg

    def get_capacidad(self):
        return self.capacidad

    def set_capacidad(self, capacidad):
        self.capacidad = capacidad

class Camion(Vehiculos):

    def __init__(self):
        self.costo_kg = [1, 2]
        super().__init__(nombre='automotor', velocidad=80, capacidad=30000, costofijo=30, costoporkm=5, costoporkg=0)

    def get_costoporkg(self):
        raise Exception('Invalid method')

    def calcular_costo(self, distancia, carga):
        if carga < 15000:
            costo_kg = self.get_costo_kg()[0]
        else:
            costo_kg = self.get_costo_kg()[1]
        costo = self.get_costofijo() + self.get_costoporkm() * distancia + costo_kg * carga
        return costo

    def get_costo_kg(self):
        return self.costo_kg

    def set_costo_kg(self, costo_kg):
        self.costo_kg = costo_kg

class Tren(Vehiculos):

    def __init__(self):
        self.costo_km = [20, 15]
        super().__init__(nombre='ferroviario', velocidad=100, capacidad=150000, costofijo=100, costoporkm=0, costoporkg=3)

    def get_costo_km(self, distancia):
        if distancia < 200:
            return self.get_costo_km()[0]
        else:
            return self.get_costo_km()[1]

    def calcular_costo(self, distancia):
        costoporkm = self.get_get_costo_km()(distancia)
        return self.get_costofijo() + costoporkm * distancia

    def get_costo_km(self):
        return self.costo_km

    def set_costo_km(self, costo_km):
        self.costo_km = costo_km

class Barco(Vehiculos):

    def __init__(self):
        super().__init__(nombre='maritimo', velocidad=40, capacidad=100000, costofijo=[500, 1500], costoporkm=15, costoporkg=2)

    def get_costofijo(self, tipo):
        if tipo == 'fluvial':
            return self.get_costofijo()[0]
        elif tipo == 'maritimo':
            return self.get_costofijo()[1]
        else:
            raise Exception('Invalid parameter')

    def calcular_costo(self, distancia, tipo):
        costo_fijo = self.get_get_costofijo()(tipo)
        return costo_fijo + self.get_costoporkm() * distancia

class Avion(Vehiculos):

    def __init__(self):
        self.velocidades = {'bueno': 600, 'malo': 400}
        super().__init__(nombre='aereo', velocidad=None, capacidad=5000, costofijo=750, costoporkm=40, costoporkg=10)

    def determinar_clima(self, prob_mal_tiempo):
        if random.random() > float(prob_mal_tiempo):
            return 'bueno'
        else:
            return 'malo'

    def get_velocidad(self, prob_mal_tiempo):
        clima = self.get_determinar_clima()(prob_mal_tiempo)
        return self.get_velocidades()[clima]

    def calcular_tiempo(self, distancia, prob_mal_tiempo):
        velocidad = self.get_get_velocidad()(prob_mal_tiempo)
        return distancia / velocidad

    def calcular_costo(self, distancia):
        return self.get_costofijo() + self.get_costoporkm() * distancia

    def get_velocidades(self):
        return self.velocidades

    def set_velocidades(self, velocidades):
        self.velocidades = velocidades

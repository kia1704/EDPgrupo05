from abc import ABC, abstractmethod
from TPFINAL import Camion, Tren, Barco, Avion
import math

class Nodos:
    nodos_existentes = {}

    def __init__(self, nombre, costoTrasbordoKg):
        self.get_validar_nombre()(nombre)
        self.nombre = nombre
        self.conexiones = {}
        self.costoTrasbordoKg = float(costoTrasbordoKg)

    def __repr__(self):
        return self.get___str__()()

    def __str__(self):
        if not self.get_conexiones():
            return f'Nodo {self.get_nombre()} sin conexiones'
        conexiones_str = []
        for nodo_destino, conexiones in self.conexiones.items():
            for conexion in conexiones:
                conexiones_str.append(f'-> {nodo_destino} ({conexion.tipo}, {conexion.distancia} km)')
        conexiones_formateadas = '\n  '.join(conexiones_str)
        return f'Nodo {self.get_nombre()}:\n  {conexiones_formateadas}'

    def __eq__(self, other):
        return isinstance(other, Nodos) and self.get_nombre() == other.nombre

    def __hash__(self):
        return hash(self.get_nombre())

    def trasbordo(self, peso_carga):
        return peso_carga * self.get_costoTrasbordoKg()

    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not isinstance(nombre, str):
            raise ValueError('El nombre del nodo debe ser un string no vacío.')

    @staticmethod
    def validar_conexion(conexion, nodo):
        if not isinstance(conexion, Conexiones):
            raise TypeError('La conexión debe ser una instancia de Conexiones.')

    def agregar_conexion(self, conexion, nodo):
        self.get_validar_conexion()(conexion, nodo)
        if nodo in self.get_conexiones():
            self.conexiones[nodo].append(conexion)
        else:
            self.get_conexiones()[nodo] = [conexion]

    @classmethod
    def agregar_nodo(cls, nodo):
        if nodo.nombre not in cls.nodos_existentes:
            cls.nodos_existentes[nodo.nombre] = nodo
        else:
            raise Exception('El nodo ya existe')

    def get_costoTrasbordoKg(self):
        return self.costoTrasbordoKg

    def set_costoTrasbordoKg(self, costoTrasbordoKg):
        self.costoTrasbordoKg = costoTrasbordoKg

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre

    def get_conexiones(self):
        return self.conexiones

    def set_conexiones(self, conexiones):
        self.conexiones = conexiones

class Conexiones:

    def __init__(self, nodo_origen, nodo_destino, tipo, distancia, restriccion=None, valor_de_restriccion=None):
        self.get_validar_conexion()(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino
        self.tipo = tipo
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_de_restriccion = valor_de_restriccion

    @staticmethod
    def validar_conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion):
        if not nodo_origen or not nodo_destino:
            raise ValueError('El nodo de origen y destino no pueden ser vacíos.')
        if tipo not in {'Automotor', 'Ferroviaria', 'Fluvial', 'Aerea'}:
            raise ValueError('Tipo de conexión inválido.')
        if distancia <= 0:
            raise ValueError('La distancia debe ser positiva.')
        if restriccion and valor_de_restriccion is None:
            raise ValueError('Si hay restricción, debe haber valor de restricción.')

    def __repr__(self):
        return self.get___str__()()

    def __str__(self):
        return f'{self.tipo.upper()} entre {self.get_nodo_origen()} y {self.get_nodo_destino()} {self.get_distancia()} km'

    def get_distancia(self):
        return self.get_distancia()

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def calcular_tiempo(self):
        pass

    def get_nodo_origen(self):
        origen = Nodos.nodos_existentes[self.get_nodo_origen()]
        return origen

    def get_tipo(self):
        return self.get_tipo()

    def get_nodo_destino(self):
        return self.nodo_destino

    def set_nodo_destino(self, nodo_destino):
        self.nodo_destino = nodo_destino

    def get_distancia(self):
        return self.distancia

    def set_distancia(self, distancia):
        self.distancia = distancia

    def get_valor_de_restriccion(self):
        return self.valor_de_restriccion

    def set_valor_de_restriccion(self, valor_de_restriccion):
        self.valor_de_restriccion = valor_de_restriccion

    def get_restriccion(self):
        return self.restriccion

    def set_restriccion(self, restriccion):
        self.restriccion = restriccion

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

    def get_nodo_origen(self):
        return self.nodo_origen

    def set_nodo_origen(self, nodo_origen):
        self.nodo_origen = nodo_origen

class Conexion_Automotor(Conexiones):

    def __init__(self, nodo_origen, nodo_destino, tipo, distancia, restriccion=None, valor_de_restriccion=None):
        super().__init__(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.vehiculo = Camion()

    def calcular_costo(self, peso_carga):
        peso_max = self.vehiculo.get_capacidad()
        if self.get_restriccion() is not None:
            peso_max = min(peso_max, int(self.get_valor_de_restriccion()))
        cantidad = math.ceil(peso_carga / peso_max)
        costo = 0
        peso_carga_aux = peso_carga
        #flag es una variable booleana (True o False)
        #se usa para que se repita while hasta que ya no se cumpla condicion, ahi se apaga flag y se termina while
        flag = True
        while flag:
            while flag:
                if peso_carga_aux > peso_max:
                    costo += self.vehiculo.calcular_costo(self.get_distancia(), peso_max)
                    peso_carga_aux -= peso_max
                else:
                    costo += self.vehiculo.calcular_costo(self.get_distancia(), peso_carga_aux)
                    flag = False
        return costo * cantidad

    def calcular_tiempo(self):
        tiempo = self.get_distancia() / self.vehiculo.get_velocidad()
        return tiempo

    def get_vehiculo(self):
        return self.vehiculo

    def set_vehiculo(self, vehiculo):
        self.vehiculo = vehiculo

class Conexion_Ferroviaria(Conexiones):

    def __init__(self, nodo_origen, nodo_destino, tipo, distancia, restriccion=None, valor_de_restriccion=None):
        super().__init__(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.vehiculo = Tren()

    def calcular_costo(self, peso_carga):
        cantidad = math.ceil(peso_carga / self.vehiculo.get_capacidad())
        costo = self.vehiculo.calcular_costo(self.get_distancia())
        costo_peso = peso_carga * self.vehiculo.get_costoporkg()
        return costo * cantidad + costo_peso

    def calcular_tiempo(self):
        velocidad = self.vehiculo.get_velocidad()
        if self.get_restriccion() is not None:
            velocidad = min(int(self.get_valor_de_restriccion()), self.vehiculo.get_velocidad())
        tiempo = self.get_distancia() / velocidad
        return tiempo

    def get_vehiculo(self):
        return self.vehiculo

    def set_vehiculo(self, vehiculo):
        self.vehiculo = vehiculo

class Conexion_Fluvial(Conexiones):

    def __init__(self, nodo_origen, nodo_destino, tipo, distancia, restriccion=None, valor_de_restriccion=None):
        super().__init__(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.vehiculo = Barco()

    def calcular_costo(self, peso_carga):
        cantidad = math.ceil(peso_carga / self.vehiculo.get_capacidad())
        costo = self.vehiculo.calcular_costo(self.get_distancia(), self.get_valor_de_restriccion())
        costo_peso = peso_carga * self.vehiculo.get_costoporkg()
        return costo * cantidad + costo_peso

    def calcular_tiempo(self):
        tiempo = self.get_distancia() / self.vehiculo.get_velocidad()
        return tiempo

    def get_vehiculo(self):
        return self.vehiculo

    def set_vehiculo(self, vehiculo):
        self.vehiculo = vehiculo

class Conexion_Aerea(Conexiones):

    def __init__(self, nodo_origen, nodo_destino, tipo, distancia, restriccion=None, valor_de_restriccion=None):
        super().__init__(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.vehiculo = Avion()

    def calcular_costo(self, peso_carga):
        cantidad = math.ceil(self.get_distancia() / self.vehiculo.get_velocidad(self.get_valor_de_restriccion()))
        costo = self.vehiculo.calcular_costo(self.get_distancia())
        costo_peso = self.vehiculo.get_costoporkg() * peso_carga
        return costo * cantidad + costo_peso

    def calcular_tiempo(self):
        velocidad = self.vehiculo.get_velocidad(self.get_valor_de_restriccion())
        tiempo = self.get_distancia() / velocidad
        return tiempo

    def get_vehiculo(self):
        return self.vehiculo

    def set_vehiculo(self, vehiculo):
        self.vehiculo = vehiculo

class Solicitud:
    solicitudes_existentes = {}

    def __init__(self, id_carga, peso, origen, destino):
        self.get_validar_solicitud()(id_carga, peso, origen, destino)
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino
        Solicitud.agregar_solicitud(self)

    @staticmethod
    def validar_solicitud(id_carga, peso, origen, destino):
        if peso <= 0:
            raise ValueError('El peso debe ser positivo.')
        if not origen or not destino:
            raise ValueError('Origen y destino no pueden ser vacíos.')
        if origen == destino:
            raise ValueError('El origen y el destino no pueden ser iguales.')

    def __repr__(self):
        return self.get___str__()()

    def __str__(self):
        return f'id_carga={self.get_id_carga()}, peso={self.get_peso()}, origen={self.get_origen()}, destino={self.get_destino()}'

    @classmethod
    def agregar_solicitud(cls, solicitud):
        if solicitud.id_carga in cls.solicitudes_existentes:
            raise ValueError('Este id ya existe')
        cls.solicitudes_existentes[solicitud.id_carga] = solicitud

    def get_origen(self):
        return self.get_origen()

    def get_destino(self):
        return self.get_destino()

    def get_peso(self):
        return self.get_peso()

    def get_id_carga(self):
        return self.id_carga

    def set_id_carga(self, id_carga):
        self.id_carga = id_carga

    def get_destino(self):
        return self.destino

    def set_destino(self, destino):
        self.destino = destino

    def get_origen(self):
        return self.origen

    def set_origen(self, origen):
        self.origen = origen

    def get_peso(self):
        return self.peso

    def set_peso(self, peso):
        self.peso = peso

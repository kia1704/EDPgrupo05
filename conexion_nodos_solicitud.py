class Nodos:
    nodos_existentes={}
    def __init__(self,nombre ):
        self.validar_nombre(nombre)

        self.nombre=nombre
        self.conexiones = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self.conexiones:
            return f"Nodo {self.nombre} sin conexiones"
        
        conexiones_str = []
        for nodo_destino, conexiones in self.conexiones.items():
            for conexion in conexiones:
                conexiones_str.append(f"-> {nodo_destino} ({conexion.tipo}, {conexion.distancia} km)")
        
        conexiones_formateadas = "\n  ".join(conexiones_str)
        return f"Nodo {self.nombre}:\n  {conexiones_formateadas}"


    def __eq__(self, other):
        return isinstance(other, Nodos) and self.nombre == other.nombre

    def __hash__(self):
        return hash(self.nombre)

    @staticmethod
    def validar_nombre(nombre):
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre del nodo debe ser un string no vacío.")
    
    @staticmethod
    def validar_conexion(conexion, nodo):
        if not isinstance(conexion, Conexiones):
            raise TypeError("La conexión debe ser una instancia de Conexiones.")

    def agregar_conexion(self, conexion, nodo):
        self.validar_conexion(conexion, nodo)
        if nodo in self.conexiones:
            self.conexiones[nodo].append(conexion) 
        else:
            self.conexiones[nodo] = [conexion]

    @classmethod
    def agregar_nodo(cls,nodo):
        if nodo.nombre not in cls.nodos_existentes:
            cls.nodos_existentes[nodo.nombre] = nodo
        else:
            raise Exception("El nodo ya existe")




class Conexiones:

    def __init__(self, nodo_origen, nodo_destino,tipo, distancia, restriccion=None,valor_de_restriccion=None): # el tipo, restriccion y valor de restriccion  chequear porque hay dos formas de hacerlo
        self.validar_conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion)
        self.nodo_origen = nodo_origen 
        self.nodo_destino = nodo_destino
        self.tipo = tipo
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_de_restriccion= valor_de_restriccion

    @staticmethod
    def validar_conexion(nodo_origen, nodo_destino, tipo, distancia, restriccion, valor_de_restriccion):
        if not nodo_origen or not nodo_destino:
            raise ValueError("El nodo de origen y destino no pueden ser vacíos.")
        if tipo not in {"Automotor", "Ferroviaria", "Fluvial", "Aerea"}:
            raise ValueError("Tipo de conexión inválido.")
        if distancia <= 0:
            raise ValueError("La distancia debe ser positiva.")
        if restriccion and valor_de_restriccion is None:
            raise ValueError("Si hay restricción, debe haber valor de restricción.")
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.tipo.upper()} entre {self.nodo_origen} y {self.nodo_destino} {self.distancia} km"
 
    
class Solicitud:
    solicitudes_existentes = {}

    def __init__(self, id_carga, peso, origen, destino):
        self.validar_solicitud(id_carga, peso, origen, destino)
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino
        Solicitud.agregar_solicitud(self)

    @staticmethod
    def validar_solicitud(id_carga, peso, origen, destino):
        if peso <= 0:
            raise ValueError("El peso debe ser positivo.")
        if not origen or not destino:
            raise ValueError("Origen y destino no pueden ser vacíos.")
        if origen == destino:
            raise ValueError("El origen y el destino no pueden ser iguales.")
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"id_carga={self.id_carga}, peso={self.peso}, origen={self.origen}, destino={self.destino}"
    
    
    @classmethod
    def agregar_solicitud(cls, solicitud):
        if solicitud.id_carga in cls.solicitudes_existentes:
            raise ValueError("Este id ya existe")
        cls.solicitudes_existentes[solicitud.id_carga] = solicitud

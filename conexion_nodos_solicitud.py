class Nodos:
    nodos_existentes={}
    def __init__(self,nombre ):
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

    def agregar_conexion(self, conexion, nodo):
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
        
        self.nodo_origen = nodo_origen 
        self.nodo_destino = nodo_destino
        self.tipo = tipo
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_de_restriccion= valor_de_restriccion

    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.tipo.upper()} entre {self.nodo_origen} y {self.nodo_destino} {self.distancia} km"
    



class Solicitud:
    solicitudes_existentes = {}

    def __init__(self, id_carga, peso, origen, destino):
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"id_carga={self.id_carga}, peso={self.peso}, origen={self.origen}, destino={self.destino}"
    
    
    @classmethod
    def agregar_solicitud (cls,solicitud):
        if solicitud.id_carga in cls.solicitudes_existentes:
            raise ValueError ("Este id ya existe")
        cls.solicitudes_existentes[solicitud.id_carga]=solicitud

class Rutas:

    def __init__(self, tipo, conexiones, costo, tiempo):
        self.tipo = tipo
        self.conexiones = conexiones
        self.costo = costo
        self.tiempo = tiempo

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        conexiones_str = "\n".join(str(conexion) for conexion in self.conexiones)
        return f"Ruta tipo {self.tipo}:\n{conexiones_str}\nCosto: {self.costo}\nTiempo: {self.tiempo}"




class Nodos:
    nodos_existentes={}
    def __init__(self,nombre ):
        self.nombre=nombre

    def __repr__(self):
        return self.nombre
    
    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return isinstance(other, Nodos) and self.nombre == other.nombre

    def __hash__(self):
        return hash(self.nombre)

    @classmethod
    def agregar_nodo(cls,nodo):
        if nodo.nombre not in cls.nodos_existentes:
            cls.nodos_existentes[nodo.nombre] = nodo
        else:
            raise Exception("El nodo ya existe")




class Conexiones:
    Conexiones_existentes= {}

    def __init__(self, nodo_origen, nodo_destino,tipo, distancia, restriccion=None,valor_de_restriccion=None): # el tipo, restriccion y valor de restriccion  chequear porque hay dos formas de hacerlo
        
        self.nodo_origen = nodo_origen 
        self.nodo_destino = nodo_destino
        self.tipo = tipo
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_de_restriccion= valor_de_restriccion
    
    #def __repr__(self):
    #    return (f"Conexiones({self.nodo_origen} -> {self.nodo_destino}, "
    #            f"tipo={self.tipo}, distancia={self.distancia} km, "
    #            f"restriccion={self.restriccion}, valor={self.valor_de_restriccion})")
    
    def __repr__(self):
        desc=(f"{self.tipo.upper()} de {self.nodo_origen} a {self.nodo_destino}, ({self.distancia} km ")
        if self.restriccion is not None:
            desc += f", restricción: {self.restriccion}"
            if self.valor_de_restriccion is not None: 
                desc+= f" = {self.valor_de_restriccion})"

        return desc
    
    
    def __str__(self):
        return self.__repr__()
    
    @classmethod
    def agregar_conexion(cls, conexion):
        if conexion.nodo_origen not in cls.Conexiones_existentes:
            cls.Conexiones_existentes[conexion.nodo_origen]= []
        cls.Conexiones_existentes[conexion.nodo_origen].append([conexion])
        #print(f"conexion agregada: {conexion}")
        #print(cls.Conexiones_existentes)

nodo1=Nodos("Zarate")
nodo2=Nodos("Junin")
nodo3=Nodos("Mar del Plata")
nodo4=Nodos("Buenos Aires")        

Conexion1=Conexiones(nodo1,nodo4, "ferroviario", 85 , "velocidad maxima", 80 )
Conexion2=Conexiones(nodo2,nodo3, "Maritimo", 500 , "fluvial")
Conexiones.agregar_conexion(Conexion1)
Conexiones.agregar_conexion(Conexion2)
for origen, lista in Conexiones.Conexiones_existentes.items():
     for origen, lista in Conexiones.Conexiones_existentes.items():
        print(f"{origen}:")
        for c in lista:
            print(f"  - {c}")


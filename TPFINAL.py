import math
import random
class Vehiculos:
    def __init__(self,nombre, velocidad, capacidad, costofijo, costoporkm, costoporkg):
        self.nombre = nombre
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.costofijo = costofijo
        self.costoporkm = costoporkm
        self.costoporkg = costoporkg
        
    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nombre):
        self.nombre = nombre
    
    def get_velocidad(self):
        return self.velocidad

    def get_capacidad(self):
        return self.capacidad

    def get_costofijo(self):
        return self.costofijo

    def get_costoporkm(self):
        return self.costoporkm

    def get_costoporkg(self):
        return self.costoporkg

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

   
    def calcular_costo(self, distancia, carga):
        return self.costofijo + self.costoporkm * distancia + self.costoporkg * carga

    def calcular_tiempo(self, distancia):
        return distancia / self.velocidad

    
class Nodos:
    nodos_existentes={}
    def __init__(self,nombre ):
        self.nombre=nombre
    @classmethod
    def agregar_nodo(cls,nodo):
        if nodo.nombre not in cls.nodos_existentes:
            cls.nodos_existentes[nodo.nombre] = nodo
        else:
            raise Exception("El nodo ya existe")
       
        
class Conexiones:
    Conexiones_existentes:{}
    def __init__(self, nodo_origen, nodo_destino, distancia, restriccion,valor_de_restriccion): # el tipo, restriccion y valor de restriccion  chequear porque hay dos formas de hacerlo
        self.distancia=distancia
        self.origen = nodo_origen 
        self.destino = nodo_destino
        self.distancia = distancia
        self.restriccion = restriccion
        self.valor_de_restriccion= valor_de_restriccion
    
    @classmethod
    def agregar_conexion(cls, conexion):
        cls.Conexion_existentes[conexion.nodo_origen]= []


class Camion(Vehiculos):
    def __init__(self):
        self.costo_kg = [1, 2]
        super().__init__(nombre="Camion", velocidad=80, capacidad=30000, costofijo=30, costoporkm=5, costoporkg=0)

           
    def get_costoporkg (self):
        raise Exception ("Invalid method")
    
    def calcular_costo(self, distancia, carga):
        if carga < 15000:
            costo_kg = self.costo_kg[0]
        else:
            costo_kg = self.costo_kg[1]

        cantidad = math.ceil(carga / self.capacidad)
        return cantidad * (self.costofijo + self.costoporkm * distancia + costo_kg * carga)

    
              
class Tren (Vehiculos):
    def __init__(self): 
        self.costoporkm = [20, 15]
        super().__init__(nombre= "Tren", velocidad=100, capacidad=150000, costofijo=100, costoporkm=0, costoporkg=3)

    def get_costoporkm(self, distancia):
       if distancia < 200 :
            return self.costoporkm[0] 
       else:
           return self.costoporkm[1]
       
    def calcular_costo(self, distancia, carga):
        costo_km = self.get_costoporkm(distancia)
        return self.costofijo + costo_km * distancia + self.costoporkg * carga   
       
    
    # preguntar def get_costoporkm (self):
        # raise Exception ("Invalid method")
    


class Barco (Vehiculos):
    def __init__(self): 
        super().__init__(nombre="Barco",velocidad=40,capacidad=100000,costofijo=[500,1500],costopokm=15,costoporkg=2)  
    

    def get_costofijo(self, tipo):
       if tipo=="fluvial" :
            return self.costofijo[0] 
       elif tipo=="maritimo":
           return self.costofijo[1]
       else:
           raise Exception ("Invalid parameter")
       
    def get_costopfijo(self):
        raise Exception ("Invalid method")
    
    def calcular_costo(self, distancia, carga, tipo="fluvial"):
        costo_fijo = self.get_costofijo(tipo)
        return costo_fijo + self.costoporkm * distancia + self.costoporkg * carga


class Avion(Vehiculos):
    def __init__(self): 
        self.velocidades = {"bueno": 600, "malo": 400}
        super()._init_(nombre= "Avion", velocidad = None ,capacidad=5000,costofijo=750,costoporkm=40, costoporkg=10)
    
    def determinar_clima(self, prob_mal_tiempo):
        """
        Retorna 'bueno' o 'malo' según la probabilidad de mal clima.
        """
        if random.random() > prob_mal_tiempo:
            return "bueno"
        else:
            return "malo"

    def get_velocidad(self, prob_mal_tiempo):
        clima = self.determinar_clima(prob_mal_tiempo)
        return self.velocidades[clima]

    def calcular_tiempo(self, distancia, prob_mal_tiempo):
        velocidad = self.get_velocidad(prob_mal_tiempo)
        return distancia / velocidad

    def calcular_costo(self, distancia, carga):
        return self.costofijo + self.costoporkm * distancia + self.costoporkg * carga

class Solicitud:
    def __init__(self, id_carga, peso, origen, destino):
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino
        
vehiculos_disponibles = [Camion(),Tren(), Barco(), Avion()]    
    




 #todo trayecto se hace con el mismo vehiculo, no puedo cambiar entre un nodo y  

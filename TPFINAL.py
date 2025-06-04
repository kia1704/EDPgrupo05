class Vehiculos:
    def _init_(self, velocidad, capacidad,costofijo,costoporkm, costoporkg,tipo,modo):
        self.velocidad=velocidad
        self.capacidad=capacidad
        self.costofijo=costofijo
        self.costoporkm=costoporkm
        self.costoporkg=costoporkg
        self.tipo=tipo
        self.modo=modo

    def calcular_costo(self,distancia,carga,cantidad_vehiculos):
        return cantidad_vehiculos*(self.costofijo + self.costoporkm * distancia + self.costoporkg *carga)
   
    def calcular_tiempo(self,distancia):
        return distancia / self.velocidad
    
class Nodos:
    def _init_(self,nombre ):
        self.nombre=nombre
        self.conexiones= set()
        
    def agregar_conexion(self, conexion):
        self.conexiones.add(conexion)
        
class Conexiones:
    def _init_(self, nodo_origen, nodo_destino, modo, distancia, restriccion):
        self.distancia=distancia
        self.origen = nodo_origen
        self.destino = nodo_destino
        self.modo = modo
        self.distancia = distancia
        self.restriccion = restriccion


class Camion(Vehiculos):
    def _init_(self):
        super()._init_(nombre= "Camion", modo='automotor', velocidad=80, capacidad=30000, costo_fijo=30, costo_km=5, costo_kg=1)


               
class Tren (Vehiculos):
    def _init_(self): 
        super()._init_(nombre="Tren", modo="Ferroviario", velocidad=100, capacidad=150000, costofijo=100, costoporkm=20, costoporkg=3)
    
    def calcular_tiempo(self,distancia,velocidad_max=None):
        V=min(self.velocidad,velocidad_max) if velocidad_max else self.velocidad
        return distancia/V
    
class Barco (Vehiculos):
    def _init_(self): 
        super()._init_(velocidad=40,capacidad=100000,costofijo=500,costopokm=15,costoporkg=2,tipo="Barco",modo="maritimo")       

class Avion(Vehiculos):
    def _init_(self): 
        super._init_(velocidad=600,capacidad=5000,costofijo=750,costoporkm=40, costoporkg=10,tipo="Avion",modo="Aereo")
    
    def calcular_tiempo(self,distancia,probabilidad_clima =None):
        v=self.velocidad
        if probabilidad_clima:
            v*=(1-probabilidad_clima) #reduce velocidad esperada
        return distancia/v
    
vehiculos_disponibles = [Camion(),Tren(), Barco(), Avion()]


 #todo trayecto se hace con el mismo vehiculo, no puedo cambiar entre un nodo y otro


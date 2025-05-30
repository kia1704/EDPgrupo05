class Vehiculos:
    def __init__(self, velocidad, capacidad,costofijo,costoporkm, costoporkg,nombre,modo):
        self.velocidad=velocidad
        self.capacidad=capacidad
        self.costofijo=costofijo
        self.costoporkm=costoporkm
        self.costoporkg=costoporkg
        self.nombre=nombre
        self.modo=modo

class Nodos:
    def __init__(self,nombre ):
        self.nombre=nombre
        self.conexiones= set()
        
    def agregar_conexion(self, conexion):
        self.conexiones.add(conexion)
        
class conexiones:
    def __init__(self, nodo_origen, nodo_destino, modo, distancia):
        self.distancia=distancia
        self.origen = nodo_origen
        self.destino = nodo_destino
        self.modo = modo
        self.distancia = distancia
               


        
 #todo trayecto se hace con el mismo vehiculo, no puedo cambiar entre un nodo y otro       
        
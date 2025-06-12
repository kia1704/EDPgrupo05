from conexion_nodos_solicitud import Nodos
from conexion_nodos_solicitud import Conexiones
from conexion_nodos_solicitud import Solicitud
from LectorCSV import LectorCSV



lector = LectorCSV()
lector.leer_csv("nodos.csv", "nodo")
lector.leer_csv("conexiones.csv", "conexion")
lector.leer_csv("solicitud.csv", "solicitud")

print(Conexiones.Conexiones_existentes)
print(Nodos.nodos_existentes)
print(Solicitud.solicitudes_existentes)


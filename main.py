from conexion_nodos_solicitud import Nodos
from conexion_nodos_solicitud import Conexiones
from LectorCSV2 import LectorCSV2

from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador

lector = LectorCSV2()
lector.leer_csv("nodos.csv", "nodo")
lector.leer_csv("conexiones.csv", "conexion")
lector.leer_csv("solicitudes.csv", "solicitud")


#print("Nodos existentes:")
# for nombre, nodo in Nodos.nodos_existentes.items():
#     print(nodo)
#     print("-" * 40)


print(Solicitud.solicitudes_existentes)

for solicitud in Solicitud.solicitudes_existentes.values():
    print(Planificador.evaluar_mejores_rutas(solicitud.origen,solicitud.destino,solicitud.peso))




#   automotor=Planificador.evaluar_rutas_automotor(solicitud.origen,solicitud.destino,solicitud.peso)
#   maritimo=Planificador.evaluar_rutas_maritimo(solicitud.origen,solicitud.destino,solicitud.peso)
#   ferroviaria=Planificador.evaluar_rutas_ferroviario(solicitud.origen,solicitud.destino,solicitud.peso)
#   aerea=Planificador.evaluar_rutas_aerea(solicitud.origen,solicitud.destino,solicitud.peso)
  

#   print(automotor)
#   print(maritimo)
#   print(ferroviaria)
#   print(aerea)
    






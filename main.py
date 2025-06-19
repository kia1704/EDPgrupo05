#from conexion_nodos_solicitud import Nodos
#from conexion_nodos_solicitud import Conexiones
from LectorCSV2 import LectorCSV2
from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador
from graficos import GraficadorRuta

#falta generar las validaciones necesarias
lector = LectorCSV2()
lector.leer_csv("nodos.csv", "nodo")
lector.leer_csv("conexiones.csv", "conexion")
lector.leer_csv("solicitudes.csv", "solicitud")



for solicitud in Solicitud.solicitudes_existentes.values():
    
    resultado=Planificador.evaluar_mejores_rutas(solicitud.origen,solicitud.destino,solicitud.peso)
    print(resultado)
    mejor_ruta = resultado["Mejor ruta por costo (tipo, info)"]  # o por tiempo

    if mejor_ruta:
        ruta_info = mejor_ruta[1] 
        graficador = GraficadorRuta(ruta_info)
        graficador.graficar()
    else:
        print("No se encontró una ruta óptima para graficar.")






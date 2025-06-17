from conexion_nodos_solicitud import Nodos
from conexion_nodos_solicitud import Conexiones
from LectorCSV2 import LectorCSV2

from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador

lector = LectorCSV2()
lector.leer_csv("nodos.csv", "nodo")
lector.leer_csv("conexiones.csv", "conexion")
lector.leer_csv("solicitudes.csv", "solicitud")


# print("Nodos existentes:")
# for nombre, nodo in Nodos.nodos_existentes.items():
#     print(nodo)
#     print("-" * 40)


rutas,nodos = Planificador.encontrar_rutas("Zarate", "Mar_del_Plata", "Ferroviaria")

print("Rutas encontradas Ferroviaria:")
for ruta in rutas:
    print("Ruta:")
    print(ruta)

rutas = Planificador.encontrar_rutas("Zarate", "Mar_del_Plata", "Automotor")

print("Rutas encontradas Automotor:")
for ruta in rutas:
    print("Ruta:")
    print(ruta)

rutas = Planificador.encontrar_rutas("Zarate", "Mar_del_Plata", "Fluvial")

print("Rutas encontradas Fluvial:")
for ruta in rutas:
    print("Ruta:")
    print(ruta)

rutas = Planificador.encontrar_rutas("Zarate", "Mar_del_Plata", "Aerea")

print("Rutas encontradas Aerea:")
for ruta in rutas:
    print("Ruta:")
    print(ruta)


print("\nSolicitudes existentes:")
for solicitud in Solicitud.solicitudes_existentes.values():
    print(solicitud)
    
from Graficos import Itinerario
from TPFINAL import Camion, Tren , Barco, Avion  

vehiculos_por_tipo = {
    "Automotor": Camion,
    "Ferroviaria": Tren,
    "Fluvial": Barco,
    "Aerea": Avion
}

print("\n--- Generación de gráfico para la primera solicitud con ruta válida ---")

graficado = False  # bandera para cortar la iteración 

for solicitud in Solicitud.solicitudes_existentes.values():
    if graficado:
        continue

    origen = solicitud.origen
    destino = solicitud.destino
    tipo = solicitud.tipo_transporte
    peso = solicitud.peso_kg

    rutas, _ = Planificador.encontrar_rutas(origen, destino, tipo)

    if rutas:
        clase_vehiculo = vehiculos_por_tipo.get(tipo)
        if clase_vehiculo:
            vehiculo = clase_vehiculo()
            ruta_elegida = rutas[0]
            itinerario = Itinerario(ruta_elegida)
            itinerario.graficar(vehiculo, peso)
            graficado = True





from conexion_nodos_solicitud import Conexiones, Solicitud, Nodos
import math
import random

class Planificador:
    def __init__(self, vehiculos_disponibles):
        self.vehiculos = vehiculos_disponibles

    def encontrar_rutas(self, origen, destino):
        rutas_posibles = []
        self._explorar_rutas(origen, destino, [], set([origen]), rutas_posibles)
        return rutas_posibles

    def _explorar_rutas(self, actual, destino, recorrido, visitados, rutas_posibles):
        if actual == destino:
            rutas_posibles.append(list(recorrido))
            return

        for conexion in Conexiones.Conexiones_existentes.get(actual, []):
            if conexion.nodo_destino in visitados:
                continue

            recorrido.append(conexion)
            visitados.add(conexion.nodo_destino)
            self._explorar_rutas(conexion.nodo_destino, destino, recorrido, visitados, rutas_posibles)
            recorrido.pop()
            visitados.remove(conexion.nodo_destino)

    def evaluar_rutas(self, solicitud):
        rutas = self.encontrar_rutas(solicitud.origen, solicitud.destino)
        opciones_validas = []

        for ruta in rutas:
            for vehiculo in self.vehiculos:
                if not vehiculo.ruta_valida(ruta, solicitud.peso):
                    continue

                cantidad = vehiculo.cantidad_necesaria(solicitud.peso)
                distancia = sum(c.distancia for c in ruta)
                velocidad = vehiculo.velocidad_real(distancia)

                tiempo = distancia / velocidad
                costo = vehiculo.calcular_costo_ruta(ruta, solicitud.peso, cantidad)

                opciones_validas.append({
                    "ruta": ruta,
                    "vehiculo": vehiculo.nombre,
                    "costo": costo,
                    "tiempo": tiempo,
                    "cantidad_vehiculos": cantidad
                })

        if opciones_validas:
            return (
                min(opciones_validas, key=lambda x: x["costo"]),
                min(opciones_validas, key=lambda x: x["tiempo"])
            )
        return None, None

import math
from conexion_nodos_solicitud import Conexiones, Nodos
from TPFINAL import Camion, Tren, Barco, Avion

import math
from conexion_nodos_solicitud import Conexiones
from TPFINAL import Camion, Tren, Barco, Avion

class Planificador:
    @staticmethod
    def encontrar_rutas(origen, destino, tipo_transporte, ruta_actual=None, nodos_visitados=None, rutas_encontradas=None):
        if ruta_actual is None:
            ruta_actual = []
        if nodos_visitados is None:
            nodos_visitados = set()
        if rutas_encontradas is None:
            rutas_encontradas = []

        nodos_visitados.add(origen)

        if origen == destino:
            rutas_encontradas.append(list(ruta_actual))
        else:
            for nodo_vecino, conexiones in Nodos.nodos_existentes[origen].conexiones.items():
                for conexion in conexiones:
                    if conexion.tipo.lower() != tipo_transporte.lower():
                        continue
                    if nodo_vecino in nodos_visitados:
                        continue

                    ruta_actual.append(conexion)

                    Planificador.encontrar_rutas(nodo_vecino, destino, tipo_transporte, ruta_actual, nodos_visitados, rutas_encontradas)

                    ruta_actual.pop()

        nodos_visitados.remove(origen)

        return rutas_encontradas
    
#Zarate,Junin,Automotor,185,peso_max,15000
    @staticmethod
    def evaluar_rutas_automotor(origen, destino, peso_carga):
            resultados = []

            camion = Camion()

            rutas = Planificador.encontrar_rutas(origen, destino, "automotor")

            peso_max = camion.capacidad

            for ruta in rutas:
                for conexion in ruta:
                    if conexion.restriccion == "peso maximo":
                        peso_max = min(peso_max, conexion.valor_de_restriccion)

                #continuar

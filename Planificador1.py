import math
from conexion_nodos_solicitud import Conexiones
from TPFINAL import Camion, Tren, Barco, Avion

class Planificador:
    @staticmethod
    def encontrar_rutas(origen, destino, ruta_actual=None, nodos_visitados=None, rutas_encontradas=None):
        if ruta_actual is None:
            ruta_actual = []
        if nodos_visitados is None:
            nodos_visitados = set()
        if rutas_encontradas is None:
            rutas_encontradas = []

        if origen == destino:
            rutas_encontradas.append(list(ruta_actual))
            return

        for conexion in Conexiones.Conexiones_existentes.get(origen, []):
            siguiente = conexion.nodo_destino
            if siguiente in nodos_visitados:
                continue

            ruta_actual.append(conexion)
            nodos_visitados.add(siguiente)

            Planificador.encontrar_rutas(siguiente, destino, ruta_actual, nodos_visitados, rutas_encontradas)

            ruta_actual.pop()
            nodos_visitados.remove(siguiente)

    @staticmethod
    def evaluar_rutas(origen, destino, peso_carga, vehiculos_disponibles):
        rutas_encontradas = []
        Planificador.encontrar_rutas(origen, destino, [], set([origen]), rutas_encontradas)
        resultados = []

        for ruta in rutas_encontradas:
            for vehiculo in vehiculos_disponibles:
                puede = True

                for conexion in ruta:
                    if conexion.tipo.lower() not in vehiculo.nombre.lower():
                        puede = False
                        break
                    if conexion.restriccion == "velocidad maxima" and vehiculo.velocidad > conexion.valor_de_restriccion:
                        puede = False
                        break
                    if conexion.restriccion == "peso maximo" and peso_carga > conexion.valor_de_restriccion:
                        puede = False
                        break

                if not puede:
                    continue

                cantidad = math.ceil(peso_carga / vehiculo.capacidad)
                distancia_total = sum(conexion.distancia for conexion in ruta)

                if isinstance(vehiculo, Camion):
                    costo = vehiculo.calcular_costo(distancia_total, peso_carga)
                    tiempo = distancia_total / vehiculo.velocidad

                elif isinstance(vehiculo, Tren):
                    costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga)
                    tiempo = distancia_total / vehiculo.velocidad

                elif isinstance(vehiculo, Barco):
                    tipo = ruta[0].tipo.lower()
                    costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga, tipo=tipo)
                    tiempo = distancia_total / vehiculo.velocidad

                elif isinstance(vehiculo, Avion):
                    tiempo = vehiculo.calcular_tiempo(distancia_total, prob_mal_tiempo=0.3)
                    costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga)

                resultados.append({
                    "ruta": ruta,
                    "vehiculo": vehiculo.nombre,
                    "costo": costo,
                    "tiempo": tiempo,
                    "cantidad_vehiculos": cantidad
                })

        if resultados:
            mas_barata = min(resultados, key=lambda x: x["costo"])
            mas_rapida = min(resultados, key=lambda x: x["tiempo"])
            return mas_barata, mas_rapida
        else:
            return None, None

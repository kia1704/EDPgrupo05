import math
from conexion_nodos_solicitud import Conexiones, Nodos
from TPFINAL import Camion, Tren, Barco, Avion





class Planificador:  
    @staticmethod
    def validar_nodo(nombre):
        if nombre not in Nodos.nodos_existentes:
            raise ValueError(f"El nodo '{nombre}' no existe en la red.")

    @staticmethod
    def validar_tipo_transporte(tipo):
        if tipo.lower() not in ["automotor", "ferroviaria", "fluvial", "aerea"]:
            raise ValueError(f"Tipo de transporte '{tipo}' no válido.")

    @staticmethod
    def validar_peso(peso):
        if peso <= 0:
            raise ValueError("El peso de carga debe ser positivo.")
        
    @staticmethod
    def encontrar_rutas(origen, destino, tipo_transporte, ruta_actual=None, nodos_visitados=None, rutas_encontradas=None):
        Planificador.validar_nodo(origen)
        Planificador.validar_nodo(destino)
        Planificador.validar_tipo_transporte(tipo_transporte)

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
                for conexion in filter(lambda conexion: conexion.tipo.lower() == tipo_transporte.lower(), conexiones):
                    if nodo_vecino in nodos_visitados:
                        continue
                    if not isinstance(conexion, Conexiones):
                        raise TypeError("Cada tramo de la ruta debe ser una instancia de Conexiones.")
                    
                    ruta_actual.append(conexion)

                    Planificador.encontrar_rutas(nodo_vecino, destino, tipo_transporte, ruta_actual, nodos_visitados, rutas_encontradas)

                    ruta_actual.pop()

        nodos_visitados.remove(origen)

        return rutas_encontradas

    @staticmethod
    def evaluar_rutas_automotor(origen, destino, peso_carga):
        resultados = []
        
        camion = Camion()
        rutas = Planificador.encontrar_rutas(origen, destino, "automotor")
        
        for ruta in rutas:
            peso_carga_aux = peso_carga
            distancia_total = 0
            peso_max = camion.capacidad
            tramos = 0
            graf_c = []
            graf_t = []

            for conexion in ruta:
                distancia_total += conexion.distancia
                tramos += 1
                if conexion.restriccion == "peso maximo":
                    peso_max = min(peso_max, conexion.valor_de_restriccion)
                tiempo_tramo = conexion.distancia / camion.get_velocidad()
                costo_tramo = camion.calcular_costo(conexion.distancia, peso_carga, 1)
                graf_c.append((conexion.distancia, costo_tramo))
                graf_t.append((conexion.distancia, tiempo_tramo))

            cantidad = math.ceil(peso_carga / peso_max)
            costo = 0
            flag = True
            while flag:
                if peso_carga_aux > peso_max:
                    costo += camion.calcular_costo(distancia_total, peso_max, tramos)
                    peso_carga_aux -= peso_max
                else:
                    costo += camion.calcular_costo(distancia_total, peso_carga_aux, tramos)
                    flag = False

            tiempo = distancia_total / camion.get_velocidad()
            resultados.append({
                "ruta": ruta,
                "cantidad": cantidad,
                "peso maximo utilizado": peso_max,
                "costo": costo,
                "tiempo": tiempo,
                "distancia vs tiempo": graf_t,
                "distancia vs costo": graf_c
            })

        if resultados:
            mejor_por_costo = min(resultados, key=lambda r: r["costo"])
            mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
            mejor_por_costo = None
            mejor_por_tiempo = None

        return {
            "Mejor costo automotor": mejor_por_costo,
            "Mejor tiempo automotor": mejor_por_tiempo
        }

    @staticmethod
    def evaluar_rutas_maritimo(origen, destino, peso_carga):
        resultados = []
        
        barco = Barco()
        rutas = Planificador.encontrar_rutas(origen, destino, "fluvial")
        cantidad = math.ceil(peso_carga / barco.capacidad)

        for ruta in rutas:
            distancia_total = 0
            costo_ruta = 0
            graf_c = []
            graf_t = []

            for conexion in ruta:
                distancia_total += conexion.distancia
                costo_tramo = barco.calcular_costo(conexion.distancia, conexion.valor_de_restriccion)
                costo_ruta += costo_tramo
                tiempo_tramo = conexion.distancia / barco.get_velocidad()
                graf_c.append((conexion.distancia, costo_tramo))
                graf_t.append((conexion.distancia, tiempo_tramo))

            costo_peso = barco.get_costoporkg() * peso_carga
            tiempo = distancia_total / barco.get_velocidad()
            resultados.append({
                "ruta": ruta,
                "cantidad": cantidad,
                "costo": costo_peso + (costo_ruta * cantidad),
                "tiempo": tiempo,
                "distancia vs tiempo": graf_t,
                "distancia vs costo": graf_c
            })

        if resultados:
            mejor_por_costo = min(resultados, key=lambda r: r["costo"])
            mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
            mejor_por_costo = None
            mejor_por_tiempo = None

        return {
            "Mejor costo maritimo": mejor_por_costo,
            "Mejor tiempo maritimo": mejor_por_tiempo
        }

    @staticmethod
    def evaluar_rutas_ferroviario(origen, destino, peso_carga):
        resultados = []
        tren = Tren()
        rutas = Planificador.encontrar_rutas(origen, destino, "ferroviaria")
        cantidad = math.ceil(peso_carga / tren.capacidad)

        for ruta in rutas:
            distancia_total = 0
            tiempo_total = 0
            costo_ruta = 0
            graf_c = []
            graf_t = []

            for conexion in ruta:
                distancia_total += conexion.distancia
                if conexion.restriccion is not None:
                    velocidad = min(int(conexion.valor_de_restriccion), tren.get_velocidad())
                else:
                    velocidad = tren.get_velocidad()
                tiempo_tramo = conexion.distancia / velocidad
                tiempo_total += tiempo_tramo
                costo_tramo = tren.calcular_costo(conexion.distancia)
                costo_ruta += costo_tramo
                graf_c.append((conexion.distancia, costo_tramo))
                graf_t.append((conexion.distancia, tiempo_tramo))

            costo_peso = tren.get_costoporkg() * peso_carga
            resultados.append({
                "ruta": ruta,
                "cantidad": cantidad,
                "costo": costo_peso + (costo_ruta * cantidad),
                "tiempo": tiempo_total,
                "distancia recorrida": distancia_total,
                "distancia vs tiempo": graf_t,
                "distancia vs costo": graf_c
            })

        if resultados:
            mejor_por_costo = min(resultados, key=lambda r: r["costo"])
            mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
            mejor_por_costo = None
            mejor_por_tiempo = None

        return {
            "Mejor costo ferroviario": mejor_por_costo,
            "Mejor tiempo ferroviario": mejor_por_tiempo
        }

    @staticmethod
    def evaluar_rutas_aerea(origen, destino, peso_carga):
        resultados = []
        avion = Avion()
        rutas = Planificador.encontrar_rutas(origen, destino, "aerea")
        cantidad = math.ceil(peso_carga / avion.capacidad)

        for ruta in rutas:
            distancia_total = 0
            tiempo_total = 0
            graf_c = []
            graf_t = []

            for conexion in ruta:
                distancia_total += conexion.distancia
                velocidad = avion.get_velocidad(conexion.valor_de_restriccion)
                tiempo_tramo = conexion.distancia / velocidad
                tiempo_total += tiempo_tramo
                costo_tramo = avion.calcular_costo(conexion.distancia)
                graf_c.append((conexion.distancia, costo_tramo))
                graf_t.append((conexion.distancia, tiempo_tramo))

            costo_peso = avion.get_costoporkg() * peso_carga
            costo_total = avion.calcular_costo(distancia_total)
            resultados.append({
                "ruta": ruta,
                "cantidad": cantidad,
                "costo": costo_peso + (costo_total * cantidad),
                "tiempo": tiempo_total,
                "velocidad": velocidad,
                "distancia vs tiempo": graf_t,
                "distancia vs costo": graf_c
            })

        if resultados:
            mejor_por_costo = min(resultados, key=lambda r: r["costo"])
            mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
            mejor_por_costo = None
            mejor_por_tiempo = None

        return {
            "Mejor costo aereo": mejor_por_costo,
            "Mejor tiempo aereo": mejor_por_tiempo
        }

    def evaluar_mejores_rutas(origen, destino, peso_carga):
        automotor = Planificador.evaluar_rutas_automotor(origen, destino, peso_carga)
        ferroviario = Planificador.evaluar_rutas_ferroviario(origen, destino, peso_carga)
        maritimo = Planificador.evaluar_rutas_maritimo(origen, destino, peso_carga)
        aereo = Planificador.evaluar_rutas_aerea(origen, destino, peso_carga)

        resultados = [
            ("automotor", automotor),
            ("ferroviario", ferroviario),
            ("maritimo", maritimo),
            ("aereo", aereo)
        ]

        mejores_costo = list(
            map(
                lambda tv: (tv[0], tv[2]),
                filter(
                    lambda tv: tv[2] is not None and "costo" in tv[1],
                    (
                        (tipo, clave, valor)
                        for tipo, resultado in resultados
                        for clave, valor in resultado.items()
                    )
                )
            )
        )

        mejores_tiempo = list(
            map(
                lambda tv: (tv[0], tv[2]),
                filter(
                    lambda tv: tv[2] is not None and "tiempo" in tv[1],
                    (
                        (tipo, clave, valor)
                        for tipo, resultado in resultados
                        for clave, valor in resultado.items()
                    )
                )
            )
        )

        mejor_por_costo = min(mejores_costo, key=lambda r: r[1]["costo"]) if mejores_costo else None
        mejor_por_tiempo = min(mejores_tiempo, key=lambda r: r[1]["tiempo"]) if mejores_tiempo else None

        return {
            "Mejor ruta por costo (tipo, info)": mejor_por_costo,
            "Mejor ruta por tiempo (tipo, info)": mejor_por_tiempo
        }

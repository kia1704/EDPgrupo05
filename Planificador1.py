import math
from conexion_nodos_solicitud import Conexiones, Nodos
from TPFINAL import Camion, Tren, Barco, Avion
from Graficos import graficar_puntos_tramos


class Planificador:  
    @staticmethod
    def validar_nodo(nombre):
        if nombre not in Nodos.nodos_existentes:
            raise ValueError(f"El nodo '{nombre}' no existe en la red.")

    

    @staticmethod
    def validar_peso(peso):
        if peso <= 0:
            raise ValueError("El peso de carga debe ser positivo.")
        
    @staticmethod
    def encontrar_rutas(origen, destino, ruta_actual=None, nodos_visitados=None, rutas_encontradas=None):
        Planificador.validar_nodo(origen)
        Planificador.validar_nodo(destino)
        

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
                    if nodo_vecino in nodos_visitados:
                        continue
                    if not isinstance(conexion, Conexiones):
                        raise TypeError("Cada tramo de la ruta debe ser una instancia de Conexiones.")
                    
                    ruta_actual.append(conexion)

                    Planificador.encontrar_rutas(nodo_vecino, destino, ruta_actual, nodos_visitados, rutas_encontradas)

                    ruta_actual.pop()

        nodos_visitados.remove(origen)

        return rutas_encontradas

    @staticmethod
    def evaluar_rutas(origen,destino,peso_carga):
        resultados=[]
        rutas= Planificador.encontrar_rutas(origen,destino)

        for ruta in rutas:
            distancia_total = 0
            graf_c = []
            graf_t = []
            costo_ruta=0
            tiempo_ruta=0
            tipo=ruta[0].get_tipo()
            costo_tras = 0
            for conexion in ruta:
                
                if conexion.get_tipo() != tipo:
                    costo_tras += conexion.get_nodo_origen().trasbordo(peso_carga)
                    tipo= conexion.get_tipo()
                
                distancia_total += conexion.get_distancia()
                costo_tramo= conexion.calcular_costo(peso_carga)
                tiempo_tramo= conexion.calcular_tiempo()
                costo_ruta+=costo_tramo
                tiempo_ruta+= tiempo_tramo
                graf_c.append((conexion.get_distancia(), costo_tramo))
                graf_t.append((conexion.get_distancia(), tiempo_tramo))
            
            resultados.append({
                "ruta": ruta,
                'distancia total': distancia_total,
                "costo": costo_ruta + costo_tras,
                "tiempo": tiempo_ruta,
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
            "Mejor costo": mejor_por_costo,
            "Mejor tiempo": mejor_por_tiempo
        }

    @staticmethod
    def procesar_solicitud(solicitud):
        print(f"\nProcesando solicitud: {solicitud}")
        try:
            resultado = Planificador.evaluar_rutas(
                solicitud.get_origen(),
                solicitud.get_destino(),
                solicitud.get_peso()
            )
        except Exception as e:
            print(f"Error al planificar rutas para la solicitud {solicitud.id_carga}: {e}")
            return

        print("Resultado de planificación:")
        Planificador.mostrar_resultado_bonito(resultado,solicitud)
        Planificador.graficar_resultados(resultado, solicitud)

    @staticmethod
    def graficar_resultados(resultado, solicitud):
        mejor_ruta_costo = resultado.get("Mejor costo")
        mejor_ruta_tiempo = resultado.get("Mejor tiempo")

        if mejor_ruta_costo:
            puntos_tiempo = mejor_ruta_costo.get("distancia vs tiempo", [])
            puntos_costo = mejor_ruta_costo.get("distancia vs costo", [])
            if puntos_tiempo:
                graficar_puntos_tramos(
                    puntos_tiempo,
                    titulo=f"Distancia acumulada vs Tiempo acumulado (Mejor por costo) [{solicitud.id_carga}]",
                    xlabel="Distancia acumulada [km]",
                    ylabel="Tiempo acumulado [horas]",
                    color='blue',
                    marker='o'
                )
            if puntos_costo:
                graficar_puntos_tramos(
                    puntos_costo,
                    titulo=f"Distancia acumulada vs Costo acumulado (Mejor por costo) [{solicitud.id_carga}]",
                    xlabel="Distancia acumulada [km]",
                    ylabel="Costo acumulado [$]",
                    color='green',
                    marker='s'
                )
        else:
            print("No se encontró una ruta óptima por costo para graficar.")

        if mejor_ruta_tiempo:
            puntos_tiempo = mejor_ruta_tiempo.get("distancia vs tiempo", [])
            puntos_costo = mejor_ruta_tiempo.get("distancia vs costo", [])
            if puntos_tiempo:
                graficar_puntos_tramos(
                    puntos_tiempo,
                    titulo=f"Distancia acumulada vs Tiempo acumulado (Mejor por tiempo) [{solicitud.id_carga}]",
                    xlabel="Distancia acumulada [km]",
                    ylabel="Tiempo acumulado [horas]",
                    color='blue',
                    marker='o'
                )
            if puntos_costo:
                graficar_puntos_tramos(
                    puntos_costo,
                    titulo=f"Distancia acumulada vs Costo acumulado (Mejor por tiempo) [{solicitud.id_carga}]",
                    xlabel="Distancia acumulada [km]",
                    ylabel="Costo acumulado [$]",
                    color='green',
                    marker='s'
                )
        else:
            print("No se encontró una ruta óptima por tiempo para graficar.")

    def mostrar_resultado_bonito(resultado, solicitud):
        print("="*50)
        print(f"Solicitud: {solicitud.id_carga} | Origen: {solicitud.origen} | Destino: {solicitud.destino} | Peso: {solicitud.peso} kg")
        print("-"*50)
        mejor_costo = resultado.get("Mejor costo")
        mejor_tiempo = resultado.get("Mejor tiempo")
        if mejor_costo:
            print(f"Mejor ruta por COSTO:")
            print(f"  Costo total: ${mejor_costo['costo']:.2f}")
            print(f"  Tiempo estimado: {mejor_costo['tiempo']:.2f} h")
            print(f"  Ruta: {[str(tramo) for tramo in mejor_costo['ruta']]}")
        else:
            print("No se encontró una ruta óptima por costo.")
        print("-"*50)
        if mejor_tiempo:
            print(f"Mejor ruta por TIEMPO:")
            print(f"  Costo total: ${mejor_tiempo['costo']:.2f}")
            print(f"  Tiempo estimado: {mejor_tiempo['tiempo']:.2f} h")
            print(f"  Ruta: {[str(tramo) for tramo in mejor_tiempo['ruta']]}")
        else:
            print("No se encontró una ruta óptima por tiempo.")
        print("="*50)

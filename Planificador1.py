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
    


            
    @staticmethod
    def evaluar_rutas_automotor(origen, destino, peso_carga):
        resultados = []

        camion = Camion()
        rutas = Planificador.encontrar_rutas(origen, destino, "automotor")

        for ruta in rutas:
            distancia_total = 0
            peso_max = camion.capacidad  # Comienza con capacidad total del camión

            for conexion in ruta:
                distancia_total += conexion.distancia

                    # Si hay una restricción de peso, se aplica para toda la ruta
                if conexion.restriccion == "peso maximo":
                    if conexion.valor_de_restriccion:
                        peso_max = min(peso_max, float(conexion.valor_de_restriccion))

            costo,cantidad = camion.calcular_costo(distancia_total,peso_carga,peso_max)    
            

            #chequear esta lista de dicc
            resultados.append({                       
                "ruta": ruta,
                "distancia_total": distancia_total,
                "peso_maximo_utilizado": peso_max,
                "cantidad_camiones": cantidad,
                "costo_total": costo
                })

        
        mejor_por_costo = min(resultados, key=lambda r: r["costo_total"])
        mejor_por_tiempo = min(resultados, key=lambda r: r["distancia_total"]) #falta dividirlo por la velocidad 

        return {"mejor_por_costo":mejor_por_costo,"mejor_por_tiempo": mejor_por_tiempo }  #capaz me conviene ponerlo en una lista o similar para cuando comparo con los otros medios despues
                                                                                            #Ademas aca estamos obteniendo unicamente el mejor costo y el mejor tiempo pero no las rutas enteras que tienen ese costo y ese tiempo

    
    
    @staticmethod
    def evaluar_rutas_maritimo(origen, destino, peso_carga):
        resultados = []

        barco = Barco()
        rutas = Planificador.encontrar_rutas(origen, destino, "maritimo")
        cantidad=math.ceil(peso_carga/barco.capacidad)
        for ruta in rutas:
            distancia_total= 0
            costo_ruta=0
            for conexion in ruta:
                distancia_total += conexion.distancia
                costo_ruta+=barco.calcular_costo(conexion.distancia,peso_carga,conexion.valor_de_restriccion)
            tiempo=distancia_total/barco.get_velocidad  #hay que hacer geters de esto para obtener
            resultados.append({"ruta":ruta ,"costo": costo_ruta * cantidad , "tiempo":tiempo})

            
        mejor_por_costo = min(resultados, key=lambda r: r["costo_total"])
        mejor_por_tiempo = min(resultados, key=lambda r: r["distancia_total"])

        return {
            "mejor_por_costo": mejor_por_costo,
            "mejor_por_tiempo": mejor_por_tiempo
        }

    @staticmethod
    def evaluar_rutas_ferroviario(origen, destino, peso_carga):
        resultados = []

        tren = Tren()
        rutas = Planificador.encontrar_rutas(origen, destino, "ferroviario")
        cantidad=math.ceil(peso_carga/tren.capacidad)
        for ruta in rutas:
            distancia_total = 0
            tiempo_total = 0
            
            for conexion in ruta:
                distancia_total += conexion.distancia
                if conexion.restriccion != None:     #es necesario este if?
                    velocidad= min(conexion.valor_de_restriccion,tren.get_velocidad)
                    tiempo_total+= (conexion.distancia/velocidad)
                else:
                    tiempo_total += (conexion.distancia / tren.get_velocidad)

            costo_ruta= tren.calcular_costo(distancia_total,peso_carga)
            resultados.append({"ruta":ruta, "cantidad":cantidad, "costo":costo_ruta *cantidad, "tiempo":tiempo_total})
        

        mejor_por_costo = min(resultados, key=lambda r: r["costo_total"])
        mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo_total"])

        return {
            "mejor_por_costo": mejor_por_costo,
            "mejor_por_tiempo": mejor_por_tiempo
        }

    @staticmethod
    def evaluar_rutas_aerea(origen,destino,peso_carga):
        resultados=[]

        avion=Avion()
        rutas=Planificador.encontrar_rutas(origen,destino,"aereo")
        cantidad = math.ceil(peso_carga/avion.capacidad)
        for ruta in rutas:
            distancia_total=0
            tiempo_total=0
            
            for conexion in ruta:
                distancia_total += conexion.distancia
                velocidad= avion.get_velocidad(conexion.prob_mal_tiempo)
                tiempo_total += (conexion.distancia/velocidad)
            
            costo_total= avion.calcular_costo(distancia_total, peso_carga)
            resultados.append({"ruta":ruta,"cantidad":cantidad, "costo":costo_total *cantidad, "tiempo":tiempo_total})
        
            

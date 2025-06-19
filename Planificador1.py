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
            peso_carga_aux=peso_carga
            distancia_total = 0
            peso_max = camion.capacidad  # Comienza con capacidad total del camión
            tramos=0
            for conexion in ruta:
                distancia_total += conexion.distancia
                tramos+=1
                    # Si hay una restricción de peso, se aplica para toda la ruta
                if conexion.restriccion == "peso maximo":
                    peso_max = min(peso_max, conexion.valor_de_restriccion)
            cantidad= math.ceil(peso_carga/peso_max)
            costo=0
            flag=True
            while flag:
                if peso_carga_aux> peso_max:
                  costo+= camion.calcular_costo(distancia_total,peso_max,tramos)
                  peso_carga_aux-=peso_max
                else:
                  costo+= camion.calcular_costo(distancia_total,peso_carga_aux,tramos)
                  flag=False
     
            tiempo=distancia_total/camion.get_velocidad()

            #chequear esta lista de dicc
            resultados.append({"ruta": ruta, "cantidad": cantidad, "peso maximo utilizado": peso_max, "costo": costo,"tiempo":tiempo})

        if resultados:
            mejor_por_costo = min(resultados, key=lambda r: r["costo"])
            mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
           mejor_por_costo= None
           mejor_por_tiempo = None 

        return {"Mejor costo automotor":mejor_por_costo,
                "Mejor tiempo automotor": mejor_por_tiempo }  #capaz me conviene ponerlo en una lista o similar para cuando comparo con los otros medios despues
                                                                                            #Ademas aca estamos obteniendo unicamente el mejor costo y el mejor tiempo pero no las rutas enteras que tienen ese costo y ese tiempo

    
    
    @staticmethod
    def evaluar_rutas_maritimo(origen, destino, peso_carga):
        resultados = []

        barco = Barco()
        rutas = Planificador.encontrar_rutas(origen, destino, "fluvial")
        cantidad=math.ceil(peso_carga/barco.capacidad)
        for ruta in rutas:
            distancia_total= 0
            costo_ruta=0
            for conexion in ruta:
                distancia_total += conexion.distancia
                costo_ruta+=barco.calcular_costo(conexion.distancia,conexion.valor_de_restriccion)

            costo_peso=barco.get_costoporkg()*peso_carga
            tiempo=distancia_total/barco.get_velocidad()  #hay que hacer geters de esto para obtener
            resultados.append({"ruta":ruta ,"cantidad":cantidad, "costo": costo_peso+(costo_ruta * cantidad) , "tiempo":tiempo})

        if resultados:    
          mejor_por_costo = min(resultados, key=lambda r: r["costo"])
          mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
          mejor_por_costo=None
          mejor_por_tiempo=None
          

        return {"Mejor costo maritimo":mejor_por_costo,"Mejor tiempo maritimo": mejor_por_tiempo }

    @staticmethod
    def evaluar_rutas_ferroviario(origen, destino, peso_carga):
        resultados = []

        tren = Tren()
        rutas = Planificador.encontrar_rutas(origen, destino,"ferroviaria")
        cantidad=math.ceil(peso_carga/tren.capacidad)
        for ruta in rutas:
            distancia_total = 0
            tiempo_total = 0
            costo_ruta=0
            print(ruta)
            for conexion in ruta:
                distancia_total += conexion.distancia
                print(conexion)
                if conexion.restriccion != None:     #es necesario este if?
                    velocidad= min(int(conexion.valor_de_restriccion),tren.get_velocidad())
                    tiempo_total+= (conexion.distancia/velocidad)
                else:
                    tiempo_total += (conexion.distancia / tren.get_velocidad())
                costo_ruta+= tren.calcular_costo(conexion.distancia)
            costo_peso=(tren.get_costoporkg()*peso_carga)
            resultados.append({"ruta":ruta, "cantidad":cantidad, "costo":costo_peso+(costo_ruta *cantidad), "tiempo":tiempo_total,"distancia recorrida":distancia_total})
        
        if resultados:
          mejor_por_costo = min(resultados, key=lambda r: r["costo"])
          mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
          mejor_por_costo =None
          mejor_por_tiempo=None
          

        return {"Mejor costo ferroviario":mejor_por_costo,"Mejor tiempo ferroviario": mejor_por_tiempo }
    
    @staticmethod
    def evaluar_rutas_aerea(origen,destino,peso_carga):
        resultados=[]

        avion=Avion()
        rutas=Planificador.encontrar_rutas(origen,destino,"aerea")
        cantidad = math.ceil(peso_carga/avion.capacidad)
        for ruta in rutas:
          distancia_total=0
          tiempo_total=0
            
          for conexion in ruta:
            distancia_total += conexion.distancia
            velocidad= avion.get_velocidad(conexion.valor_de_restriccion)
            tiempo_total += (conexion.distancia/velocidad)
        
          costo_peso= avion.get_costoporkg()*peso_carga
          costo_total= avion.calcular_costo(distancia_total)
          resultados.append({"ruta":ruta,"cantidad":cantidad, "costo":costo_peso+(costo_total *cantidad), "tiempo":tiempo_total,"velocidad":velocidad})
        
        if resultados:
          mejor_por_costo = min(resultados, key=lambda r: r["costo"])
          mejor_por_tiempo = min(resultados, key=lambda r: r["tiempo"])
        else:
          mejor_por_costo=None
          mejor_por_tiempo =None
          

        return {"Mejor costo aereo":mejor_por_costo,"Mejor tiempo aereo": mejor_por_tiempo }
            
    @staticmethod
    def evaluar_mejores_rutas(origen, destino, peso_carga):
        # Ejecuta los 4 métodos de evaluación
        automotor = Planificador.evaluar_rutas_automotor(origen, destino, peso_carga)
        ferroviario = Planificador.evaluar_rutas_ferroviario(origen, destino, peso_carga)
        maritimo = Planificador.evaluar_rutas_maritimo(origen, destino, peso_carga)
        aereo = Planificador.evaluar_rutas_aerea(origen, destino, peso_carga)

        # Juntar los mejores resultados de cada tipo
        mejores_rutas = []

        for resultado in [automotor, ferroviario, maritimo, aereo]:
            if resultado["Mejor costo automotor"] is not None:
                mejores_rutas.append(("automotor", resultado["Mejor costo automotor"]))
            elif resultado["Mejor costo ferroviario"] is not None:
                mejores_rutas.append(("ferroviario", resultado["Mejor costo ferroviario"]))
            elif resultado["Mejor costo maritimo"] is not None:
                mejores_rutas.append(("maritimo", resultado["Mejor costo maritimo"]))
            elif resultado["Mejor costo aereo"] is not None:
                mejores_rutas.append(("aereo", resultado["Mejor costo aereo"]))

        # Mejor por costo
        mejor_por_costo = min(mejores_rutas, key=lambda r: r[1]["costo"]) if mejores_rutas else None

        # Juntar los mejores por tiempo
        mejores_tiempos = []

        for resultado in [automotor, ferroviario, maritimo, aereo]:
            if resultado["Mejor tiempo automotor"] is not None:
                mejores_tiempos.append(("automotor", resultado["Mejor tiempo automotor"]))
            if resultado["Mejor tiempo ferroviario"] is not None:
                mejores_tiempos.append(("ferroviario", resultado["Mejor tiempo ferroviario"]))
            if resultado["Mejor tiempo maritimo"] is not None:
                mejores_tiempos.append(("maritimo", resultado["Mejor tiempo maritimo"]))
            if resultado["Mejor tiempo aereo"] is not None:
                mejores_tiempos.append(("aereo", resultado["Mejor tiempo aereo"]))

        # Mejor por tiempo
        mejor_por_tiempo = min(mejores_tiempos, key=lambda r: r[1]["tiempo"]) if mejores_tiempos else None

        return {
            "Mejor ruta por costo (tipo, info)": mejor_por_costo,
            "Mejor ruta por tiempo (tipo, info)": mejor_por_tiempo
        }
       

#costo,tiempo=Planificador.evaluar_rutas_automotor("Zarate", "Mar_del_Plata",70000)
#print(costo)
#print(tiempo)







# class Planificadorrr:

#     @staticmethod
#     def evaluar_rutas(origen, destino, peso_carga, vehiculos_disponibles):
#         resultados = []

#         for vehiculo in vehiculos_disponibles:
#             rutas_encontradas = Planificador.encontrar_rutas(origen, destino, vehiculo.nombre.lower())

#             for ruta in rutas_encontradas:
#                 tipos_ok = True
#                 for conexion in ruta:
#                     if conexion.tipo.lower() not in vehiculo.nombre.lower():
#                         tipos_ok = False
#                     if conexion.restriccion == "velocidad maxima" and vehiculo.velocidad > conexion.valor_de_restriccion:
#                         tipos_ok = False
#                     if conexion.restriccion == "peso maximo" and peso_carga > conexion.valor_de_restriccion:
#                         tipos_ok = False
#                 if not tipos_ok:
#                     continue

#                 cantidad = math.ceil(peso_carga / vehiculo.capacidad)
#                 distancia_total = sum(conexion.distancia for conexion in ruta)

#                 if isinstance(vehiculo, Camion):
#                     costo = vehiculo.calcular_costo(distancia_total, peso_carga)
#                     tiempo = distancia_total / vehiculo.velocidad

#                 elif isinstance(vehiculo, Tren):
#                     costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga)
#                     tiempo = distancia_total / vehiculo.velocidad

#                 elif isinstance(vehiculo, Barco):
#                     tipo = ruta[0].tipo.lower()
#                     costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga, tipo=tipo)
#                     tiempo = distancia_total / vehiculo.velocidad

#                 elif isinstance(vehiculo, Avion):
#                     tiempo = vehiculo.calcular_tiempo(distancia_total, prob_mal_tiempo=0.3)
#                     costo = cantidad * vehiculo.calcular_costo(distancia_total, peso_carga)

#                 resultados.append({
#                     "ruta": ruta,
#                     "vehiculo": vehiculo.nombre,
#                     "costo": costo,
#                     "tiempo": tiempo,
#                     "cantidad_vehiculos": cantidad
#                 })

#         if resultados:
#             mas_barata = min(resultados, key=lambda x: x["costo"])
#             mas_rapida = min(resultados, key=lambda x: x["tiempo"])
#             return mas_barata, mas_rapida
#         else:
#             return None, None


        
            

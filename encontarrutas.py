import math 
#aca importo esto pq encontre una funcion que te devuelve el entero mas grande 

def encontrar_rutas(origen, destino, ruta_actual, nodos_visitados, rutas_encontradas):
    if origen == destino:
        rutas_encontradas.append(list(ruta_actual))
        return
    for lista_conex in Conexiones.Conexiones_existentes.get(origen, []):
        conexion = lista_conex[0]
        if conexion.nodo_destino in nodos_visitados:
            continue  # No tnr cicloss
        ruta_actual.append(conexion)
        nodos_visitados.add(conexion.nodo_destino)
        encontrar_rutas(conexion.nodo_destino, destino, ruta_actual, nodos_visitados, rutas_encontradas)
        ruta_actual.pop()
        nodos_visitados.remove(conexion.nodo_destino)

def evaluar_rutas(origen, destino, peso_carga, vehiculos_disponibles):
    rutas_encontradas = []
    encontrar_rutas(origen, destino, [], set([origen]), rutas_encontradas)
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
                if peso_carga > vehiculo.capacidad:
                    pass  
            if not puede:
                continue

            cantidad_vehiculos = math.ceil(peso_carga / vehiculo.capacidad)
            distancia_total = sum(conexion.distancia for conexion in ruta)
            if isinstance(vehiculo, Camion):
                costo_total = vehiculo.calcular_costo(distancia_total, peso_carga)
                tiempo_total = distancia_total / vehiculo.velocidad
            elif isinstance(vehiculo, Tren):
                costo_total = vehiculo.costofijo + vehiculo.get_costoporkm(distancia_total) * distancia_total + vehiculo.costoporkg * peso_carga
                tiempo_total = distancia_total / vehiculo.velocidad
            elif isinstance(vehiculo, Barco):
                tipo = ruta[0].tipo.lower()
                costo_total = vehiculo.get_costofijo(tipo) + vehiculo.costopokm * distancia_total + vehiculo.costoporkg * peso_carga
                tiempo_total = distancia_total / vehiculo.velocidad
            elif isinstance(vehiculo, Avion):
                velocidad = vehiculo.velocidad[0]
                costo_total = vehiculo.costofijo + vehiculo.costoporkm * distancia_total + vehiculo.costoporkg * peso_carga
                tiempo_total = distancia_total / velocidad
            else:
                continue

            resultados.append({
                "ruta": ruta,
                "vehiculo": vehiculo.nombre,
                "costo": costo_total,
                "tiempo": tiempo_total,
                "cantidad_vehiculos": cantidad_vehiculos
            })

    if resultados:
        mas_barata = min(resultados, key=lambda x: x["costo"])
        mas_rapida = min(resultados, key=lambda x: x["tiempo"])
        return mas_barata, mas_rapida
    else:
        return None, None
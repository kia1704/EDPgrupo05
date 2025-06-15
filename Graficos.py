import matplotlib.pyplot as plt

def graficar_itinerario(itinerario, vehiculo, peso_total):
    dist_acumulada = []
    tiempo_acumulado = []
    costo_acumulado = []

    suma_dist = 0
    suma_tiempo = 0
    suma_costo = 0

    for conexion in itinerario:
        distancia = conexion.distancia

        if vehiculo.__class__.__name__ == "Avion":
            if conexion.restriccion == 'prob_mal_tiempo':
                prob = float(conexion.valor_de_restriccion)
            else:
                prob = 0
            tiempo = vehiculo.calcular_tiempo(distancia, prob)

        elif vehiculo.__class__.__name__ == "Tren":
            if conexion.restriccion == "velocidad_max":
                velocidad_real = min(vehiculo.velocidad, int(conexion.valor_de_restriccion))
                tiempo = distancia / velocidad_real
            else:
                tiempo = distancia / vehiculo.velocidad

        else:
            tiempo = distancia / vehiculo.velocidad

        costo = vehiculo.calcular_costo(distancia, peso_total)

        suma_dist += distancia
        suma_tiempo += tiempo
        suma_costo += costo

        dist_acumulada.append(suma_dist)
        tiempo_acumulado.append(suma_tiempo)
        costo_acumulado.append(suma_costo)

    plt.figure(figsize=(10, 5))
    plt.plot(tiempo_acumulado, dist_acumulada, marker='o', color='blue')
    plt.title("Distancia Acumulada vs. Tiempo Acumulado")
    plt.xlabel("Tiempo acumulado [horas]")
    plt.ylabel("Distancia acumulada [km]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(dist_acumulada, costo_acumulado, marker='s', color='green')
    plt.title("Costo Acumulado vs. Distancia Acumulada")
    plt.xlabel("Distancia acumulada [km]")
    plt.ylabel("Costo acumulado [$]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

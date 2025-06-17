import matplotlib.pyplot as plt
from TPFINAL import Avion, Tren  


class Itinerario:
    def __init__(self, conexiones):
        self.conexiones = conexiones

    def graficar(self, vehiculo, peso_total):
        dist_acumulada = []
        tiempo_acumulado = []
        costo_acumulado = []

        suma_dist = 0
        suma_tiempo = 0
        suma_costo = 0

        for conexion in self.conexiones:
            distancia = conexion.distancia

            if isinstance(vehiculo, Avion):
                prob = float(conexion.valor_de_restriccion) if conexion.restriccion == 'prob_mal_tiempo' else 0
                tiempo = vehiculo.calcular_tiempo(distancia, prob)

            elif isinstance(vehiculo, Tren):
                velocidad_real = min(vehiculo.velocidad, int(conexion.valor_de_restriccion)) if conexion.restriccion == "velocidad_max" else vehiculo.velocidad
                tiempo = distancia / velocidad_real

            else:
                tiempo = distancia / vehiculo.velocidad

            costo = vehiculo.calcular_costo(distancia, peso_total)

            suma_dist += distancia
            suma_tiempo += tiempo
            suma_costo += costo

            dist_acumulada.append(suma_dist)
            tiempo_acumulado.append(suma_tiempo)
            costo_acumulado.append(suma_costo)

        self._graficar_distancia_vs_tiempo(dist_acumulada, tiempo_acumulado)
        self._graficar_costo_vs_distancia(dist_acumulada, costo_acumulado)

    def _graficar_distancia_vs_tiempo(self, distancias, tiempos):
        plt.figure(figsize=(10, 5))
        plt.plot(tiempos, distancias, marker='o', color='blue')
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.xlabel("Tiempo acumulado [horas]")
        plt.ylabel("Distancia acumulada [km]")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def _graficar_costo_vs_distancia(self, distancias, costos):
        plt.figure(figsize=(10, 5))
        plt.plot(distancias, costos, marker='s', color='green')
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.xlabel("Distancia acumulada [km]")
        plt.ylabel("Costo acumulado [$]")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

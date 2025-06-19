import matplotlib.pyplot as plt

class GraficadorRuta:
    def __init__(self, ruta):
        """
        ruta: diccionario con las claves:
            - 'ruta': lista de conexiones (cada una con atributo 'distancia')
            - 'costo': costo total de la ruta
            - 'tiempo': tiempo total de la ruta
        """
        self.ruta = ruta

    def calcular_acumulados(self):
        conexiones = self.ruta["ruta"]
        total_distancia = sum(getattr(tramo, "distancia", 0) for tramo in conexiones)
        total_tiempo = self.ruta["tiempo"]
        total_costo = self.ruta["costo"]

        dist_acumulada = []
        tiempo_acumulado = []
        costo_acumulado = []

        suma_dist = 0
        suma_tiempo = 0
        suma_costo = 0

        for tramo in conexiones:
            d = getattr(tramo, "distancia", 0)
            suma_dist += d

            # Proporción de este tramo respecto al total
            proporcion = d / total_distancia if total_distancia > 0 else 0

            suma_tiempo += total_tiempo * proporcion
            suma_costo += total_costo * proporcion

            dist_acumulada.append(suma_dist)
            tiempo_acumulado.append(suma_tiempo)
            costo_acumulado.append(suma_costo)

        return dist_acumulada, tiempo_acumulado, costo_acumulado


    def graficar(self):
        dist_acumulada, tiempo_acumulado, costo_acumulado = self.calcular_acumulados()

        # Distancia vs Tiempo
        plt.figure(figsize=(10, 5))
        plt.plot(tiempo_acumulado, dist_acumulada, marker='o', color='blue')
        plt.title("Distancia Acumulada vs. Tiempo Acumulado")
        plt.xlabel("Tiempo acumulado [horas]")
        plt.ylabel("Distancia acumulada [km]")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Distancia vs Costo
        plt.figure(figsize=(10, 5))
        plt.plot(dist_acumulada, costo_acumulado, marker='s', color='green')
        plt.title("Costo Acumulado vs. Distancia Acumulada")
        plt.xlabel("Distancia acumulada [km]")
        plt.ylabel("Costo acumulado [$]")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

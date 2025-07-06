#DEFINITIVO
import matplotlib.pyplot as plt

def graficar_puntos_tramos(puntos, titulo, xlabel, ylabel, color='blue', marker='o'):
    """
    puntos: lista de tuplas (distancia, valor acumulado)
    titulo: título del gráfico
    xlabel: etiqueta eje X
    ylabel: etiqueta eje Y
    color: color de la curva
    marker: marcador de los puntos
    """
    distancias = [0]
    valores = [0]
    suma_dist = 0
    suma_valor = 0
    for d, v in puntos:
        suma_dist += d
        suma_valor += v
        distancias.append(suma_dist)
        valores.append(suma_valor)

    plt.figure(figsize=(10, 5))
    plt.plot(distancias, valores, marker=marker, color=color)
    for x, y in zip(distancias[1:], valores[1:]):
        plt.annotate(f"({x:.0f}, {y:.0f})", (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    

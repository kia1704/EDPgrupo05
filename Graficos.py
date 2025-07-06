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
    from itertools import accumulate
    distancias = [0] + list(accumulate(map(lambda p: p[0], puntos)))
    valores = [0] + list(accumulate(map(lambda p: p[1], puntos)))
    
    plt.plot(distancias, valores, marker=marker, color=color)
    for x, y in zip(distancias[1:], valores[1:]):
        plt.annotate(f'({x:.0f}, {y:.0f})', (x, y), textcoords='offset points', xytext=(0, 10), ha='center', fontsize=9)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    

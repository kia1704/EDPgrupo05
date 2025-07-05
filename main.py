from LectorCSV import LectorCSV2
from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador
from Graficos import graficar_puntos_tramos

def main():
    lector = LectorCSV2()
    try:
        lector.leer_csv("nodos.csv", "nodo")
        lector.leer_csv("conexiones.csv", "conexion")
        lector.leer_csv("solicitudes.csv", "solicitud")

    except Exception as e:
        print(f"Error al leer archivos CSV: {e}")
        return

    for solicitud in Solicitud.solicitudes_existentes.values():
        print(f"\nProcesando solicitud: {solicitud}")
        try:
            resultado = Planificador.evaluar_rutas(solicitud.get_origen(), solicitud.get_destino(), solicitud.get_peso())
        except Exception as e:
            print(f"Error al planificar rutas para la solicitud {solicitud.id_carga}: {e}")
            continue

        print("Resultado de planificación:")
        print(resultado)

        mejor_ruta_costo = resultado.get("Mejor ruta por costo (tipo, info)")
        mejor_ruta_tiempo = resultado.get("Mejor ruta por tiempo (tipo, info)")

        if mejor_ruta_costo and mejor_ruta_costo[1]:
            puntos_tiempo = mejor_ruta_costo[1].get("distancia vs tiempo", [])
            puntos_costo = mejor_ruta_costo[1].get("distancia vs costo", [])
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

        if mejor_ruta_tiempo and mejor_ruta_tiempo[1]:
            puntos_tiempo = mejor_ruta_tiempo[1].get("distancia vs tiempo", [])
            puntos_costo = mejor_ruta_tiempo[1].get("distancia vs costo", [])
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

if __name__ == "__main__":
    main()
    


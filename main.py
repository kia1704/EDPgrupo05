from LectorCSV import LectorCSV2
from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador


def main():
    try:
        LectorCSV2.leer_todo()
    except Exception as e:
        print(f"Error al leer archivos CSV: {e}")
        return

    for solicitud in Solicitud.solicitudes_existentes.values():
        Planificador.procesar_solicitud(solicitud)

if __name__ == "__main__":
    main()



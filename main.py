from LectorCSV import LectorCSV2
from conexion_nodos_solicitud import Solicitud
from Planificador1 import Planificador


def main():
    try:
        LectorCSV2.leer_todo()
        for solicitud in Solicitud.solicitudes_existentes.values():
            try:
                Planificador.procesar_solicitud(solicitud)
            except Exception as e:
                print(f"Error al procesar la solicitud {solicitud.id_carga}: {e}")
    except Exception as e:
        print(f"Error crítico: {e}")
        
if __name__ == "__main__":
    main()




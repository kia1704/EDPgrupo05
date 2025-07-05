#DEFINITIVO
import csv
from conexion_nodos_solicitud import Nodos, Conexion_Automotor, Conexion_Ferroviaria, Conexion_Fluvial, Conexion_Aerea, Solicitud

class LectorCSV2:
    def leer_csv(self, archivo, tipo):
        try:
            with open(archivo, newline='', encoding='utf-8') as f:
                lector = list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no fue encontrado.")
            return
        except Exception as e:
            print(f"Error al leer '{archivo}': {e}")
            return

        if tipo == "nodo":
            self.procesar_nodos(lector)
        elif tipo == "conexion":
            self.procesar_conexiones(lector)
        elif tipo == "solicitud":
            self.procesar_solicitudes(lector)
        else:
            print(f"Tipo de archivo desconocido: {tipo}")

    def procesar_nodos(self, lector):
        for row in lector:
            nombre = row['nombre']
            costoTrasbordoKg = row['costoTrasbordoKg']
            nodo = Nodos(nombre, costoTrasbordoKg)
            try:
                Nodos.agregar_nodo(nodo)
            except Exception as e:
                print(f"Nodo repetido: {nombre} - {e}")
                
    def procesar_conexiones(self, lector):
        for row in lector:
            origen = Nodos.nodos_existentes.get(row['origen'])
            destino = Nodos.nodos_existentes.get(row['destino'])
            if origen and destino:  # se fija si ninguno sea null
                tipo = row['tipo']
                try:
                    distancia = int(row['distancia_km'])
                except (ValueError, TypeError):
                    print(f"Valor inválido para 'distancia_km': {row['distancia_km']}")
                    continue
                restriccion = row.get('restriccion') or None
                valor = row.get('valor_restriccion') or None
                if valor == "":
                    valor = None
                if restriccion == "":
                    restriccion = None
                    
                if tipo == "Automotor":
                    clase_conexion = Conexion_Automotor
                elif tipo == "Ferroviaria":
                    clase_conexion = Conexion_Ferroviaria
                elif tipo == "Fluvial":
                    clase_conexion = Conexion_Fluvial
                elif tipo == "Aerea":
                    clase_conexion = Conexion_Aerea
                else:
                    print(f"Tipo de conexión desconocido: {tipo}")
                    continue

                conexion = clase_conexion(origen.nombre, destino.nombre, tipo, distancia, restriccion, valor)
                conexion2 = clase_conexion(destino.nombre, origen.nombre, tipo, distancia, restriccion, valor)

                origen.agregar_conexion(conexion, destino.nombre)
                destino.agregar_conexion(conexion2, origen.nombre)
            else:
                print(f"No se encontró el nodo origen o destino: {row['origen']} → {row['destino']}")


    def procesar_solicitudes(self, lector):
        for fila in lector:
            id_carga = fila['id_carga']
            try:
                peso = float(fila['peso_kg'])
            except (ValueError, TypeError):
                print(f"Valor inválido para 'peso_kg': {fila['peso_kg']}")
                continue
            origen = fila['origen']
            destino = fila['destino']

            if origen not in Nodos.nodos_existentes or destino not in Nodos.nodos_existentes:
                print(f"Nodo no encontrado en solicitud: {origen} → {destino}")
                continue

            solicitud = Solicitud(id_carga, peso, origen, destino)
            


import pandas as pd
from conexion_y_nodos import Nodos
from conexion_y_nodos import Conexiones

class LectorCSV:
    def leer_csv(self, archivo, tipo):

        try:
            leido = pd.read_csv(archivo)
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no fue encontrado.")
            return
        except Exception as e:
            print(f"Error al leer '{archivo}': {e}")
            return

        if tipo == "nodo":
            self.procesar_nodos(leido)
        elif tipo == "conexion":
            self.procesar_conexiones(leido)
        else:
            print(f"Tipo de archivo desconocido: {tipo}")

    def procesar_nodos(self, leido):
        for _, row in leido.iterrows():
            nombre = row['nombre']
            nodo = Nodos(nombre)
            try:
                Nodos.agregar_nodo(nodo)
            except Exception as e:
                print(f"Nodo repetido: {nombre} - {e}")

    def procesar_conexiones(self, leido):
        for _, row in leido.iterrows():
            origen = Nodos.nodos_existentes.get(row['origen'])
            destino = Nodos.nodos_existentes.get(row['destino'])
            if origen and destino: ##aca entra al if si origen y destino son nodos que existen
                tipo = row['tipo']
                distancia = row['distancia_km']
                restriccion = row['restriccion'] if 'restriccion' in row else None
                valor = row['valor_restriccion'] if 'valor_restriccion' in row else None
                #restriccion = row.get('restriccion', None)
                #valor = row.get('valor_restriccion', None)
                if pd.isna(restriccion):  ## aca se chequea si en el archivo pandas hay un Nan y lo cambia por un None
                    restriccion = None 
                if pd.isna(valor): 
                    valor = None
                conexion = Conexiones(origen, destino, tipo, distancia, restriccion, valor)
                Conexiones.agregar_conexion(conexion)
            else:
                print(f"No se encontró el nodo origen o destino: {row['origen']} → {row['destino']}")


lector = LectorCSV()
lector.leer_csv("nodos.csv", "nodo")
lector.leer_csv("conexiones.csv", "conexion")

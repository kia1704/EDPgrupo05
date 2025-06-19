import csv
from conexion_nodos_solicitud import Nodos, Conexiones, Solicitud

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
            nodo = Nodos(nombre)
            try:
                Nodos.agregar_nodo(nodo)
            except Exception as e:
                print(f"Nodo repetido: {nombre} - {e}")

#     origen,destino,tipo,distancia_km,restriccion,valor_restriccion
# Zarate,Buenos_Aires,Ferroviaria,85,velocidad_max,80
# Zarate,Junin,Ferroviaria,185,,
# Junin,Azul,Ferroviaria,265,,
# Azul,Mar_del_Plata,Ferroviaria,246,,
# Buenos_Aires,Mar_del_Plata,Ferroviaria,384,,
# Zarate,Buenos_Aires,Automotor,85,,
# Zarate,Junin,Automotor,185,peso_max,15000
# Junin,Buenos_Aires,Automotor,238,,
# Junin,Azul,Automotor,265,,
# Azul,Buenos_Aires,Automotor,278,,
# Azul,Mar_del_Plata,Automotor,246,,
# Buenos_Aires,Mar_del_Plata,Automotor,384,,
# Zarate,Buenos_Aires,Fluvial,85,tipo,fluvial
# Buenos_Aires,Mar_del_Plata,Fluvial,384,tipo,maritimo
# Junin,Buenos_Aires,Aerea,238,prob_mal_tiempo,0.1
# Azul,Buenos_Aires,Aerea,278,prob_mal_tiempo,0.2
# Buenos_Aires,Mar_del_Plata,Aerea,384,prob_mal_tiempo,0.3


    def procesar_conexiones(self, lector):
        for row in lector:
            origen = Nodos.nodos_existentes.get(row['origen'])
            destino = Nodos.nodos_existentes.get(row['destino'])
            if origen and destino: #se fija si ningunsea null
                tipo = row['tipo']
                distancia = int(row['distancia_km']) #fijarse una excepcion 
                restriccion = row.get('restriccion') or None
                valor = row.get('valor_restriccion') or None
                if valor == "":
                    valor = None
                if restriccion == "":
                    restriccion = None
                conexion = Conexiones(origen.nombre, destino.nombre, tipo, distancia, restriccion, valor)
                #print(f"--> {conexion}")
                #print(f"-----------")
                origen.agregar_conexion(conexion,destino.nombre)
                destino.agregar_conexion(conexion,origen.nombre)
            else:
                print(f"No se encontró el nodo origen o destino: {row['origen']} → {row['destino']}")

    def procesar_solicitudes(self, lector):
        for fila in lector:
            id_carga = fila['id_carga']
            peso = float(fila['peso_kg'])
            origen = fila['origen']
            destino = fila['destino']

            if origen not in Nodos.nodos_existentes or destino not in Nodos.nodos_existentes:
                print(f"Nodo no encontrado en solicitud: {origen} → {destino}")
                continue

            solicitud = Solicitud(id_carga,peso,origen,destino)
            Solicitud.agregar_solicitud(solicitud)

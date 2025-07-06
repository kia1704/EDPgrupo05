# EDPgrupo05
En este repositorio se encuentran todos los archivos que conforman el Trabajo Practico Final. Los siguientes son:
- "main.py" : Ejecuta el programa completo procesando solicitudes y mostrando resultados.
- "LectorCSV.py" : El encargado de leer los archivos csv y cargar nodos, conexiones y solicitudes correspondientes.
- "conexion_nodos_solicitud.py" : Define nodos, conexiones y solicitudes, y cómo se relacionan.
- "Planificador1.py" : Planifica rutas posibles según costo y tiempo.
- "Graficos.py" : Genera gráficos de costo y tiempo acumulado por ruta.
- "TPFINAL.py": Define los vehículos que componen el sistema y sus caracteristicas

IMPORTANTE: 
Para que el programa funcione correctamente se debe crear el sistema de nodos y conexiones deseados por el usuario. Para esto debe asegurarse que los archivos csv en donde se enceuntra la informacion de los nodos, conexiones y de las solicitudes a procesar se encuentren en la misma carpeta que los archivos que componen el programa y que sus nombres sean: "nodos.csv", "conexiones.csv" y "solicitudes.csv" respectivamente.

LOGICA DEL PROGRAMA:
Luego de armar el sistema con los nodos y conexiones especificados en los archivos correspondientes, el programa tomara cada solicitud indicada en el archivo de solicitudes y mostrara para cada una de ellas sus especificaciones y detallara las mejores rutas optimizadas en base a distintos KPIs, en este caso costo y tiempo. Luego de esta informacion se presentara el siguiente mensaje en la consola "Presione ENTER para ver los graficos de esta solicitud..." y de esta forma se podran visualizar para dicha solicitud 4 graficos ( distancia acumulada vs tiempo y vs costo para cada ruta optimizada). De esta forma se repite el mismo proceso para cada una de las solicitudes.

🚂🚛🚢✈️ A PLANIFICAR!!

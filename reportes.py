"""
Funcion del modulo reportes:
El modulo de reportes funciona a traves de filtros de fechas, utiliza un archivo json para leer las ventas y los totales, que se escriben cuando se realiza una venta
-Funcion para generar reporte historico: lee y procesa el producto más vendido, el total y emite la fecha en la que se hizo el reporte
-Funcion para generar reporte mensual: a partir de un año y mes en especifico, lee y procesa el producto más vendido, el total de ventas y emite la fecha en el que se hizo el reporte
-Funcion para generar el reporte entre dos fechas: apartir de un rango de 2 fechas , fecha de inicio y fecha de termino, procesa y lee el producto más vendido, el total y emite la fecha 
en el que se hizo el reporte.
"""
from datetime import datetime
import json
from collections import Counter

class NoExistenVentas(ValueError):
    pass

def generar_reporte_historico():
    try:#try para ejecutar el codigo y lanzar except en caso de errores
        with open('ventas.json','r', encoding= 'utf-8') as archivo: #lee el archivo ventas
            ventas = json.load(archivo) #carga el archivo json
            buscar_productos = [producto for buscar_ventas in ventas for producto in buscar_ventas['productos']]#busca productos con comprension de listas
            if not buscar_productos: #si no encuentra productos
                raise NoExistenVentas("No se ha encontrado ninguna venta")#error, no hay productos
            contador = Counter(producto["nombre_producto"] for producto in buscar_productos)#de lo contrario usamos counter para contar cuantos productos hay
            producto_mas_vendido = contador.most_common(1)[0][0]#usamos most_common de la libreria Counter para saber el primero mas vendido
            todas_las_ventas = [float(venta['total']) for venta in ventas]#recorremos total en ventas buscando todos los totales y la convertimos en float
            total_ventas= sum(todas_las_ventas) #sumamos to la lista de totales
            fecha_reporte = datetime.now()#obtenemos la fecha y hora actual
            imprimir_reporte = fecha_reporte.strftime('%Y-%m-%d %H:%M:%S')#la convertimos en string para que pueda ser impresa y le damos formato deseado
            return{#retornamos los datos que necesitamos como diccionario
                "producto_mas_vendido": producto_mas_vendido,
                "total_ventas":total_ventas,
                "fecha": imprimir_reporte
            }
    except NoExistenVentas as e:#capturamos el primer error y damos un mensaje personalizado "no hay productos"
        print(f"Error: {e}")
        return None#no retorna nada
    except FileNotFoundError:#capturamos el segundo error
        raise FileNotFoundError("Error: No existe el archivo ventas o no puede ser creado")#damos mensaje personalizado("no existe el archivo o no puede ser creado")

def reporte_filtrar_por_mes(fecha):#reporte para filtrar por mes, con el parametro fecha que se obtiene desde el input que ingresa el usuario    
    try:#try para manejar errores
        datetime.strptime(fecha, '%Y-%m')
    except ValueError:
            raise ValueError("Error de formato: use YYYY-MM")
    try:
        with open('ventas.json', 'r', encoding='utf-8') as file_ventas: #abrimos el json como file_ventas
            cargar_ventas = json.load(file_ventas)#cargamos el json con load y con nombre cargar_ventas
            producto_filtrado = [#creamos una lista para filtrar el producto mas vendido entre fechas
                producto #aqui se almacenaran los datos
                for venta in cargar_ventas  #recorremos venta en cargar_ventas que seria el primer scope del json o el primer nivel por asi decirlo donde esta la fecha
                if venta['fecha_de_venta'].startswith(fecha) # si venta coincide"fecha" coincide con la fecha ingresada "startswith(fecha)"
                for producto in venta['productos'] #Se recorre producto en venta en el nivel de ['productos'] del json
            ]# se cierra la lista
            contar_productos = Counter(producto['nombre_producto'] for producto in producto_filtrado) #usamos Counter para contar los productos, recorremos con producto para obtener el ['nombre_producto'] en ventas_filtradas("aqui ya se filtra por fecha")
            producto_mas_vendido = contar_productos.most_common(1)[0][0]#luego usamos most_common para obtener el que mas se repite y asi obtener el mas vendido
            ventas_filtradas = [ #creamos otra lista para filtrar el total de las ventas dentro del parametro fecha
                venta for venta in cargar_ventas#recorremos venta en cargar ventas , osea recorremos solo el primer nivel del json o primer scope que es donde esta el "total"
                if venta ['fecha_de_venta'].startswith(fecha)#si venta ["fecha_de_venta"] coincide con la fecha ingresada .startswith(fecha)
            ] #se cierra 
            suma_ventas_totales = sum(float(venta['total']) for venta in ventas_filtradas) #sumamos el total, recorriendo venta y obtener ['total'] dentro de ventas_filtradas ("ya filtrada por fechas")
            fecha_de_reporte = datetime.now()#creamos la fecha para el reporte
            imprimir_el_reporte = fecha_de_reporte.strftime('%Y-%m-%d %H:%M:%S') #pasamos la fecha de objeto a string
            return{ #retornamos los valores como diccionarios
            "producto_mas_vendido" : producto_mas_vendido,
            "total_ventas" : suma_ventas_totales,
            "fecha" : imprimir_el_reporte
            }
        if not producto_filtrado: #si no se encuentra productos
            raise NoExistenVentas(f"No se encontraron ventas en esta fecha {fecha}") #lanzamos un error personalizado
    except NoExistenVentas as f:#capturamos el error como f
        print(f)#imprimimos el mensaje 
def reporte_filtrar_por_2_fechas(fecha_inicio, fecha_termino): #funcion para filtrar el reporte entre fechas ingresadas en input por el usuario
        fecha_inicio = datetime.strptime(fecha_inicio,'%Y-%m-%d') #se convierte la fecha obtenida a objeto ,"se convierte a objeto para poder comparar con horas minutos y segundos en el json, ya que con string no es posible, sin necesidad de que el usuario ingrese hora. minutos y segundos"
        fecha_termino = datetime.strptime(fecha_termino +' 23:59:59', '%Y-%m-%d %H:%M:%S')#se convierte a objeto la fecha de temrino, y se la adicionan 23:59:59 h,m y segundos para que la fecha termino no sea exactamente 'HASTA' que comienze el dia de termino , sino que las horas restante hasta antes de comenzar el siguiente dia 
        try: #try para manejo de errores
            with open('ventas.json', 'r', encoding='utf-8') as file: #abrimos el jsn como file
                todas_las_ventas = json.load(file) #cargamos el json como todas_las_ventas ("al usar load pasa de ser una lista de diccionario a objetos python")
                if not todas_las_ventas: #si no encuentra ventas
                    raise FileExistsError("No se encuentra el archivo ventas.json") #se lanza este error
                venta_filtradas = [ #creamos esta comprension de lista, 'una comprension de lista es una lista creada a partir de otras pero se aplican condiciones , en este caso se filtra por fecha creando una nueva lista, espero que se entienda'
                    venta #variable temporal que almacenara los datos
                    for venta in todas_las_ventas #recorremos venta en todas_las_ventas
                    if fecha_inicio <= datetime.strptime(venta['fecha_de_venta'],'%Y-%m-%d %H:%M:%S') <= fecha_termino
                ]#se convierte a objeto, 'fecha_de_venta' obtenida de 'venta', para comprar entre rangos
                #y dice asi: si venta['fecha_de venta'] esta entre fecha_inicio y fecha_de termino.
                productos_filtrados = [ #creamos otra lista ("comprension de lista")
                    producto #creamos la variable temporal producto
                    for venta in todas_las_ventas #recorremos venta en todas_las_ventas
                    for producto in venta['productos'] #recorremos producto en venta['productos'] ("en el nivel de productos del json") 
                    if fecha_inicio <= datetime.strptime(venta['fecha_de_venta'],'%Y-%m-%d %H:%M:%S') <= fecha_termino
                ]#comparemos que venta['fecha_de_venta'] este entre los rangos a comparar, fecha_inicio y fecha_termino
                if not productos_filtrados: #si no hay productos
                    raise print("No se encontraron productos en ese rango de fechas")#lanzamos el error
                filtrar_productos = Counter(producto['nombre_producto'] for producto in productos_filtrados)# contamos con 'Counter' el producto más vendido, recorremos producto en productos filtrados "lista ya filtrada", producto obtiene el valor de ['nombre_producto'], asi counter cuenta el producto mas repetido a través del nombre
                producto_mas_vendido = filtrar_productos.most_common(1)[0][0]# con most_common obtenmos el que mas se repite y ese seria el que mas se ha vendido
                total_ventas = sum(float(valor['total']) for valor in venta_filtradas) #sumamos el total recorriendo valor en ventas_filtradas, valor['total']obtiene el valor de total y luego se convierte a un valor float y sumamos con 'sum'
                obtener_fecha = datetime.now()# creamos la fecha para el reporte emitido
                fecha_del_reporte = obtener_fecha.strftime('%Y-%m-%d %H:%M:%S') #lo convertimos a string y le damos formato
                return{#retornamos la lista de diccionarios, clave y valor
                    "producto_mas_vendido": producto_mas_vendido,
                    "total_ventas": total_ventas,
                    "fecha_del_reporte": fecha_del_reporte
                }
        except FileExistsError as g:#capturamos el error de archivo inexistente como g
            print(g) #imprimimos el mensaje del error
        except ValueError as h:#capturamos el error de valor como h
            print(h) #imprimimos el mensaje del error
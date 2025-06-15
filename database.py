import csv  # Importamos la librería csv para trabajar con archivos CSV
import json #Importamos la librería para trabajar con formatos json
from models import Producto
import os #Importamos la libreria os, que permite intereactuar con el sistema operativo, en este caso para verficar si existe un archivo
from datetime import datetime
from models import Venta
"""
Funciones del modulo:

-Funciones como  guardar_producto en formato csv
-Funcion guardar_venta para guardar las ventas en forma json
-Funcion cargar_producto para cargar productos desde un csv
*Se capturan errores para evitar que cierre abruptamente*
"""
class ProductoNoEncontradoError(Exception):
    pass
class StockNoValido(Exception):
    pass
def guardar_producto(producto):  # Creamos la función para guardar un producto
    archivo = "productos.csv" #asignamos el nombre del csv a la variable
    archivo_existe = os.path.isfile(archivo) #usa os.path.isfile para verificar si el archivo ya existe (True/Flase).
    # Abrimos (o creamos si no existe) el archivo en modo agregar, con codificación utf-8 y sin saltos de línea extra
    with open("productos.csv", "a", newline='', encoding='utf-8') as file: #abrimos el archivo en modo "a" append/agregar, si no existe, lo crea. newline ='' evita lineas en blanco extra
        escribir = csv.writer(file)  # Creamos el objeto escribir para escribir en el archivo CSV
    # Si el archivo no existe o está vacio (tamaño 0), escribe la fila de encabezados    
        if not archivo_existe or os.stat(archivo).st_size == 0: #os.stat(archivo).st_size == 0 devuelve el valor en bytes
            escribir.writerow(["Id","Nombre","Precio","Stock","Categoria","Fecha_de_actualización"])
        # Escribimos una fila con los atributos del producto.
        # Cada elemento de la lista será una columna en el archivo CSV.
        escribir.writerow([
        str(producto.id),# Convertimos el id a string por si es UUID
        producto.nombre,
        producto.precio,
        producto.stock,
        producto.categoria,
        producto.fecha_actualizacion
        ])
def guardar_venta(venta):
    # Convertimos el objeto venta a un diccionario , cada venta es un diccionario con estos atributos
    venta_dict = {  
        "id_venta": str(venta.id_venta),
        "productos": venta.productos,
        "total": str(venta.total), 
        "fecha_de_venta": venta.fecha_de_venta
    }
    # Abrimos el archivo ventas.json en modo agregar o creamos si no existe
    try:
        with open("ventas.json", "r", encoding='utf-8') as archivo:
            ventas = json.load(archivo)# Carga las ventas anteriores para no sobrescribirlas al guardar la nueva
    except FileNotFoundError:#en caso no encontrar dispara este error
        ventas = []#y crea una lista 
    ventas.append(venta_dict)#agrega las ventas(venta_dict)
    with open("ventas.json", "w", encoding='utf-8') as archivo: #escribe en el archivo ventas.json y guarda como archivo
        json.dump(ventas, archivo, ensure_ascii=False, indent=4)#guarda la lista de ventas en archivo, ensure permite caracteres espciales y indent para que sea mas legible con sangria 4

#funcion para cargar los productos desde un csv
def cargar_productos():
    productos = [] #cramos una lista donde se almacenan los datos  
    try:    
        with open("productos.csv", "r", newline="", encoding="utf-8") as archivo: #leemos el archivo y usamos newline para evitar saltos de linea demas
            lector = csv.reader(archivo) #almacenamos la lectura en variable lector
            next(lector,None) #Salta la primera fila del csv(encabezado)
            for fila in lector: #recorremos las filas de lector
                try:
                    producto = Producto( #creamos un objeto donde ira cada dato en su respectivo atributo
                    nombre = fila[1], #fila [1] el 1 representa el dato de la segunda columna
                    precio = float(fila[2]), #el dato de la tercera columna
                    stock = int(fila[3]),#el dato de la cuarta columna
                    categoria= fila[4],#el de la quinta columna
                    fecha_actualizacion= fila[5] #el de la sexta columna
                )
                    producto.id = fila[0] #el dato de la primera columna, y esta fuera del objeto ya que queremos el id que entrega el cvs, sobrescribimos el id generado por nuestro constructor por el leido del cvs al terminar cada ciclo
                except ValueError:  
                    raise ValueError("Verifique que los campos precio y stock no contengan letras")
                productos.append(producto) #finalmente agregamos nuestro objeto a la lista                
        return productos #retornamos la lista de productos
    except FileNotFoundError:
        raise FileNotFoundError("Solo se admiten archivos en formato csv")

#funcion para buscar productos
def buscar_producto(nombre):#funcion para buscar producto con el parametro nombre
    productos = cargar_productos()#utiliza la funcion cargar_producto para ver los productos del csv
    resultado = [p for p in productos if nombre.lower() in p.nombre.lower()] #utilizo comprension de lista para comprar nombres y realizar la busqueda todo en lower
    return resultado #retorno el resultado para ver los productos similares del producto buscado(nombre)

#**********Funciones del submenu Registrar venta**********

def buscar_y_seleccionar(nombre, ventas_productos_temporales): #funcion para buscar y seleccionar el producto usando el parametro nombre y 
    # el parametro  ventas_productos_temporales en menu(main) para ver el stock en tiempo real desde el csv usan esa variable se usa la funcion cargar_producsto()
    #asi se puede ver los datos en memoria y no con persistencia de datos por si el cliente cancela la venta
    try:
        productos_econtrados = [p for p in ventas_productos_temporales if nombre.lower() in p.nombre.lower()] #uso comprension de lista para buscar el producto segun el parametro, todo en lower
        seleccionado = [] #lista para guardar el producto seleccionados atraves del id
        if not productos_econtrados: #si no encuentra un nombre que coincida
            raise ProductoNoEncontradoError(f"No se ha encontrado ningun producto con {nombre}") #error , no se encuentra el producto
        for idx, resultado in enumerate(productos_econtrados, 1):#utilizo enumarate 1, uso del ciclo for para enumerar productos_encontrados comenzando externamente desde el id 1, se almacena en idx y en resultado se almacenan los productos
            print(f"ID - {idx}). {resultado}") #se imprime los productos con el id
        #input para capturar el id o 0 volver
        seleccionar_producto = int(input(f"Digite el ID del producto que desea agregar y presione enter o digite 0 para volver: ",))# input para preguntar que producto se seleccionara 
        if seleccionar_producto == 0: #si el usuario ingresa 0 
            return [] #retorna una lista vacia
        elif seleccionar_producto > len(productos_econtrados): # si el id digitado es mayor que la cantidad de productos, quiere decir que el id digitado no esta en la lista
            print("Seleccione un ID valido") #imprimimos un mensaje de id no valido
            return []#retornamos una lista vacia para evitar errores
        producto_elegido = productos_econtrados[seleccionar_producto -1]# variable para elejir el producto con el id interno correspondiente ya que comienza desde 1 por eso se le resta -1 "todo indice comienza desde el 0"
        seleccionado.append(producto_elegido) #se almacena en la lista el id seleccionado
    except ProductoNoEncontradoError as e: #capturamos el error de ProductoNoEncontradoError
        print(e) #Imprimimos mensaje de Error
    return seleccionado#Retornamos el producto seleccionado

def seleccionar_cantidad(productos_agregados): #funcion para seleccionar la cantidad del producto que se agregara
    productos_elegidos = [] #lista para retornar la tupla producto,cantidad
    try:
        for producto in productos_agregados: #recorremos los productos agregados en la funciona buscar_y_seleccionar
            print(f"Producto:{producto.nombre}| Stock Disponible:{producto.stock}| Precio:{producto.precio}")#Se imprimen los atributos del producto
            print("Digite la cantidad que desea agregar:")#imprimimos mensaje de la cantidad que quieres ingresar    
            cantidad = int(input("Ingresar cantidad: "))# input para agregar cantidad
            if cantidad <=0 :#si cantidad es menor o = 0 
                raise StockNoValido("La cantidad de Stock es menor a la existencia actual")#enviamos un error StockNoValido
            elif cantidad > producto.stock :#si cantidad es mayor a stock
                raise StockNoValido("La cantidad de Stock es mayor a la existencia actual")#enviamos un error StockNoValido
            else:#de lo contrario agregamos el producto a la lista
                productos_elegidos.append((producto,cantidad))#tupla agregada a la lista, producto y cantidad
    except StockNoValido as e:#capturamos el error de StockNoValido
        print(e)   #se imprime el mensaje
    return productos_elegidos #retornamos la lista con las tuplas de productos_elegidos

#funcion para actualiza el stock en tiempo real
def actualizar_stock_temporal(producto,cantidad,venta_productos_temporales): #parametros a utilizar, el parametro producto y cantidad se usan de la variable cantidad en menu
    for prod in venta_productos_temporales: # iteramos sobre la lista en tiempo real en memoria de ventas_productos_temporales de menu (cargar_productos())
        if producto.id == prod.id: # comparamos que los id sean iguales
            if prod.stock < cantidad: #si el stock cargado en memoria es mayor que la cantidad ingresada
                raise StockNoValido(f"La cantidad ingresada no puede ser mayor al stock actual") #error en caso de stock mayor al actual
            prod.stock -= cantidad #se resta la cantidad si todo esta bien
            return #retornamos la cantidad
    raise ProductoNoEncontradoError(f"El producto {producto} con ID: {producto.id} no coincide o no se encuentra agregado a la lista actual de productos")#error si los id no coinciden

#funcion para escribir en el archivo csv al terminar la venta
def escribir_en_csv(productos_reales):
    with open('productos.csv', 'w', newline='', encoding='utf-8') as file:
        escribir = csv.writer(file)
        escribir.writerow(["Id","Nombre","Precio","Stock","Categoria","Fecha_de_actualización"])
        for prod in productos_reales:
            escribir.writerow([
            str(prod.id),
            prod.nombre,
            prod.precio,
            prod.stock,
            prod.categoria,
            prod.fecha_actualizacion])
        
    
'''
funcion para terminar ventar:
- Se lee los datos almacenados en productos agregados.
- Se suman los valores con un total.
- Se actualiza la lista de productos ("stocks") en csv.
- Imprime venta total con productos vendidos.
- Genera venta en formato Json
'''
def terminar_venta(productos_agregados): #funcion para terminar la venta, necesita como parametro la lista de productos agregados
    productos_reales = cargar_productos() # funcion para cargar la lista de productos del csv
    total = 0 #variable para sumar el total 
    ventas_json = [] #variable para almacenar la lista de diccionario de los productos, id, cantidad,precio de la lista de productos que estan en productos_agregados, vale decir el parametro que necesita la funcion
    try:
        if not productos_agregados: #si no hay productos agregado
            raise ProductoNoEncontradoError("No se ha ingresado ningun producto.") #dispara el error 
        for prod, cant in productos_agregados: # recorremos con un for la lista de productos para obtener productos y cantidad
            ventas_json.append({"id_producto": prod.id, #almacenamos en la varaible ventas_json
                                "nombre_producto": prod.nombre,
                                "cantidad": cant,
                                "precio": prod.precio,})
            for producto_real in productos_reales : # recorremos la lista del csv
                if cant <=0: #si cantidad es <= 0 dispara el error 
                    raise StockNoValido("La cantidad debe ser mayor a 0") #el error: la cantidad debe ser mayor a 0
                if producto_real.id == prod.id : #si producto_real.id (del csv) coincide con el prod.id almacenado en memoria (productos_agregados)
                    if producto_real.stock < cant: #si producto_real.stock (stock en inventario "en csv") es mayor a la cantidad solicitada (cantidad solicitada en memoria)
                        raise StockNoValido(f"No hay sufuciente stock para {prod.nombre}, venta cancelada.") #de lo contrario lanza el error : No hay suficiente stock para X producto y se cancela la venta
                    producto_real.stock -= cant #si producto_real.stock es mayor a la cantidad solicitada, se resta la cantidad solicitada al stock disponible en csv
                    total += float(producto_real.precio * cant) #sumamos el precio real * cantidad y se almacenada en total
                    break #termina el ciclo for
            #Parte para registrar la venta en json usando la funcio guardar_venta()
        venta = Venta(productos = ventas_json, total = total) #creamos un objeto de la clase Venta, el parametro productos y total que necesita la clase Venta le damos la lista de diccionario y el total
        guardar_venta(venta) #llamamos a la funcion guardar_venta y le damos la varaible que necesita para ejecutarse en este caso "venta", y generar el json a traves de la funcion guardar_venta()
    except ProductoNoEncontradoError as e: #manejo de error de producto no encontrado, se captura el error
        print(e) #se imprime el mensaje de error
    except StockNoValido as f: #captura de error del StockNoValido
        print(f)  #se imprime el mensaje
    escribir_en_csv(productos_reales) # llamamos a la funcion escribir_en_csv para reescribir con el stock actualizado 
    print(f"Venta realizada. Total: ${total}") #imprimimos la venta

            
                
                
        
        
        
        
    
            
                
                
                
                
                
                
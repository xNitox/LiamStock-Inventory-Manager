import uuid
from datetime import datetime

"""
Clases del módulo:

Class Producto: 
-Constructor con los atributos: nombre,stock,categoria,fecha de actualizacion
y id generado aleatoriamente con la libreria uuid.
-Manejo de fechas en string y datetime.
-Método actualizar_stock : para agregar cantidad de stock .
-Método: funcion para aplicar descuento en forma de % obteniendo el precio total y precio anterior redondeado.
Class Venta:
-Constructor con los atributos: productos, total, fecha de venta y id genereado aleatoriamente con uuid.
-Manejo de fechas con string y datetime.
*Se maneja errores tanto de logica de negocio como agregar stock negativo o descuento sobre el 100% o menor que 0%
además se normmalizan las mayusculas a minusculas*
"""
class Producto:
    def __init__ (self, nombre, precio, stock, categoria, fecha_actualizacion = None):
        self.id = uuid.uuid4()#asigna un id aleatorio
        self.nombre = nombre.lower()#normalizar nombre a minusculas
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = categoria.lower()#normaliza a minuscula
        if fecha_actualizacion is None:
            self.fecha_actualizacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance (fecha_actualizacion, datetime):#si fecha viene en formato date time lo almacena como datetime
            self.fecha_actualizacion = fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S')# si viene en formato datetime lo formatea a string para darle el formato deseado 
            
        elif isinstance(fecha_actualizacion, str):#si viene en formato string lo cambia a date time
            try:
                fecha_dt = datetime.strptime(fecha_actualizacion, '%Y-%m-%d %H:%M:%S')# valida el string y lo vuelve a datetime
                self.fecha_actualizacion = fecha_dt.strftime('%Y-%m-%d %H:%M:%S') #normaliza el datetime a string
            except ValueError:
                raise ValueError("El String debe tener formato 'YYYY-MM-DD HH:MM:SS'") #raise en caso de no tener el formato
        else:
            raise ValueError("La fecha debe ser un string o datetime") #raise en caso de dato invaldio
    def __str__(self,):
        return (f"ID:{self.id}|Nombre:{self.nombre}|Precio: ${self.precio},|Stock:{self.stock}|Categoría:{self.categoria}|Fecha:{self.fecha_actualizacion}")
        #agrega más stock 
    def actualizar_stock(self, cantidad):
        if self.stock + cantidad >=0:#valida que no se ingrese numeros negativos
            self.stock += cantidad #luego agrega la cantidad
            print(f"Actualizado correctamente!"
                f"{self.stock} de {self.nombre} quedan disponibles!")
            return True
        else:
            print(f"Error: No hay suficiente stock de {self.nombre}. Stock actual: {self.stock} ")
            return False  
        #aplica un descuento al producto
    def precio_con_descuento(self, descuento):
        if not isinstance(descuento,(int, float)):#si el descuento no entra en int o float salta al raise de abajo
            try: #primero valida que sean valores de 0 a 100
                if descuento < 0 or  descuento > 100 :
                    raise ValueError("El descuento debe ser entre 0 y 100%") # usé un raise por que es un error critico , no se respeta la regla de negocio , se crea el objeto error
                else: 
                    descuento_aplicado = self.precio * (descuento/100)#se calcula  el descuento a aplicar
                    precio_final = round(self.precio - descuento_aplicado,2) #se resta el descuento al precio original y da el precio final
                    print(f"****** RESUMEN DEL DESCUENTO *****")
                    print(f"Producto : {self.nombre}")
                    print(f"Precio original: {self.precio}")
                    print(f"Descuento: ${descuento}% - {descuento_aplicado:.2f}")
                    print(f"Precio final: ${precio_final:.2f}")
                    return precio_final
            except TypeError: #manejo de error por si se ingresan string y no numeros
                print("Error: Ingrese solo numeros")
                return None # retorna none ya que requiere solo numero
            except ValueError as e: #Aqui atrapo el ValueError creado en el rais y lo manejo  (siempre buscara el ValueError mas cercano sino se crashea y cierra)
                print(f"Error {e}")
                return None #retorna none segun el error almacenado en e

class Venta:
    def __init__(self,productos,total,fecha_de_venta = None):
        self.id_venta = uuid.uuid4()
        self.productos = productos
        self.total = total
        if fecha_de_venta is None:
            self.fecha_de_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#crea la fecha y ahora actual del venta si viene sin fecha
        elif isinstance(fecha_de_venta, datetime ): #si viene en formato date time
            self.fecha_de_venta = fecha_de_venta.strftime('%Y-%m-%d %H:%M:%S') #formatea el datetime a string para darle el formato
        elif isinstance(fecha_de_venta, str):#Si viene en formato string
                try:
                    fecha_dt = datetime.strptime(fecha_de_venta, '%Y-%m-%d %H:%M:%S')  # lo pasa a datatime y formatea para validar el formato del string
                    self.fecha_de_venta = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')#lo vuelve a dejar en formato string con el mismo formato evitando errores
                except ValueError: #raise en caso de que el formato string no venga deseado
                    raise ValueError("El formato debe ser 'YYYY-MM-DD HH:MM:SS'")       
        else:#raise en caso de que no sea el tipo de dato ni string ni datetime
            raise ValueError("El fecha debe ser un string o datetime")
                








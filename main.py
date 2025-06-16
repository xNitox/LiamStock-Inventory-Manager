import database
import models
import reportes
"""
Menu interactivo para probar los modulos con opciones como:
-(1)Agregar producto en formato csv(excel)
-(2)Buscar producto por nombre, o rango de precios
-(3)Registrar venta(Actualiza stock automaticamente)
-(4)Generar un reporte con producto mas vendido, totales vendido y fecha del reporte
-(5)Salir
"""
while True:
    try:
        print(f'\n**Bienvenido a "LiamStock"**\n',
        "¡Tu guerrero contra el caos del inventario!\n",
        "Seleccione una opción:\n",
        "1- Agregar producto\n",
        "2- Buscar producto\n",
        "3- Registrar venta\n",
        "4- Generar reporte\n",
        "5- Salir")
        opcion = int(input("Opción: "))
        
        if opcion == 1:
            while True:
                try:
                    print("Presione enter para volver o continue para ingresar el producto:")
                    nombre = input("Ingrese el nombre del producto: ")
                    if nombre:
                        precio = float(input("Ingrese el precio del producto: $"))
                        stock = int(input("Ingrese la cantidad de stock disponible: "))
                        categoria = input("Ingrese la categoria del producto: ")
                    elif nombre == "":
                        print("Descansando...Zzz...")
                        break
                    print(f'\nPara ingresar el nuevo producto escriba "confirmar" y presione enter: \n'
                        f'(digite "0" para volver.)')
                    confirmar = input(":")
                    if confirmar == "confirmar":
                        producto = models.Producto(nombre,precio,stock,categoria)
                        database.guardar_producto(producto)
                        print("Producto Ingresado Exitosamente!")
                    elif confirmar == "0":
                        print("Descansando...Zzz..")
                        print("No se agregó ningun producto.")
                        break  
                except ValueError:
                    print(f"\nError: Ingrese solo números.")
                    break 
            
        elif opcion == 2:
            buscar_producto = input("Buscar: ")
            producto_buscado = database.buscar_producto(buscar_producto)
            for producto in producto_buscado:
                print(producto)
        elif opcion == 3:
            venta_productos_temporales = database.cargar_productos()
            productos_agregados = []
            while True:
                print(f"**Registrar Venta**\n",
                f"Seleccione una opción:\n",
                f"1- Agregar producto\n",
                f"2- Terminar venta\n",
                f"3- Salir")
                subopcion = int(input("Opción: "))
                if subopcion == 1:
                    while True:
                        print("Escriba el producto que desea agregar o digite 0 para volver:")
                        nombre_del_producto = input("Buscar:")
                        if nombre_del_producto == "0":
                            break
                        agregar_productos = database.buscar_y_seleccionar(nombre_del_producto,venta_productos_temporales)
                        if not agregar_productos:
                            break
                        elif agregar_productos:
                            cantidad = database.seleccionar_cantidad(agregar_productos)
                            productos_agregados.extend(cantidad)
                            for producto, cant in cantidad:
                                database.actualizar_stock_temporal(producto, cant, venta_productos_temporales)
                            print(f"¿Desea agregar más productos?\n",
                            f"1- Si",
                            f"2- No") 
                            subopcion1_1 = int(input(": ")) 
                            if subopcion1_1 == 2:
                                break
                        
                    print(f"***Liam Stock***" )   
                    for producto, cantidad in productos_agregados:
                        print(f"Producto: {producto.nombre} - Precio:{producto.precio} - Cantidad: {cantidad}")  
                elif subopcion == 2:
                    database.terminar_venta(productos_agregados)
                    break
                elif subopcion == 3:
                    break
                else:
                    print("Opción invalida")         
        elif opcion == 4:
            while True:
                try:
                    print(f"**Liam Stock**",
                    f"Despertando....Activado!\n"
                    f"Digite una opcion:\n"
                    f"1- Reporte Historico\n"
                    f"2- Filtrar por mes\n"
                    f"3- Filtrar entre fechas\n"
                    f"4- Salir")
                    subopcion4_1 = int(input("Opción: "))
                    if subopcion4_1 == 1:
                        reporte_historico = reportes.generar_reporte_historico()
                        if reporte_historico:
                            print("**** REPORTE HISTORICO GENERADO ****")
                            print(f"Produco más vendido:{reporte_historico['producto_mas_vendido']}")
                            print(f"Ventas Totales: ${reporte_historico['total_ventas']}")
                            print(f"Fecha del reporte: {reporte_historico['fecha']}")
                            print("************************************")
                        break
                    elif subopcion4_1 == 2:
                        print("Ingrese la fecha en formato YYYY-MM")
                        fecha = input(":")
                        try:
                            filtrar = reportes.reporte_filtrar_por_mes(fecha)
                            if filtrar:
                                print(f"Producto más vendido: {filtrar['producto_mas_vendido']}")
                                print(f"Ventas Totales: ${filtrar['total_ventas']}")
                                print(f"Fecha del reporte: {filtrar['fecha']}")
                            break
                        except ValueError as e:
                            print(e)
                    elif subopcion4_1 == 3:
                        fecha_inicio = input("Ingrese la fecha de inicio con el siguiente formato YYYY-MM-DD:")
                        fecha_termino = input("Ingrese la fecha de termino con el siguiente formato YYYY-MM-DD:")
                        try:
                            reporte = reportes.reporte_filtrar_por_2_fechas(fecha_inicio,fecha_termino)
                            if reporte :
                                print(f"Producto más vendido:{reporte['producto_mas_vendido']}")
                                print(f"Ventas Totales: ${reporte['total_ventas']}")
                                print(f"Fecha del reporte:{reporte['fecha_del_reporte']}")
                        except ValueError:
                            print("Formato de fecha incorrecto. Use YYYY-MM-DD")
                    elif subopcion4_1 == 4:
                        break
                except ValueError:
                    print("Error: Ingrese solo números.")
                    break   
        elif opcion == 5:
            print("Durmiendo..Zzz...")
            break
        else:
            print("\n ERROR:¡DIGITE UNA OPCIÓN VALIDA!")
    except ValueError:
        print("\n ERROR:¡INGRESE SOLO NÚMEROS!")
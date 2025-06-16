# LiamStock - Gestor de Inventario y Ventas

![GitHub repo size](https://img.shields.io/github/repo-size/xNitox/Desafio-ApResti-Foro)
![GitHub contributors](https://img.shields.io/github/contributors/xNitox/Desafio-ApResti-Foro)
![GitHub stars](https://img.shields.io/github/stars/xNitox/Desafio-ApResti-Foro?style=social)
![GitHub forks](https://img.shields.io/github/forks/xNitox/Desafio-ApResti-Foro?style=social)
![GitHub issues](https://img.shields.io/github/issues/xNitox/Desafio-ApResti-Foro)

## **Descripción del Proyecto**

**LiamStock** es una aplicación de consola desarrollada en Python para la gestión de inventario y ventas. Permite registrar productos, controlar stock, registrar ventas y generar reportes automáticos de productos más vendidos y totales de ventas, todo almacenado en archivos CSV y JSON.

---

## 📋 Descripción

LiamStock ayuda a pequeñas empresas o negocios a llevar un control eficiente de su inventario y ventas, permitiendo:
- Registrar productos y actualizar su stock.
- Registrar ventas y actualizar automáticamente el inventario.
- Buscar productos por nombre.
- Generar reportes históricos, mensuales o por rango de fechas entregando el total de ventas y productos más vendidos.
- Persistencia de datos en archivos CSV y JSON.

---

## 🚀 Funcionalidades

- **Agregar producto:** Permite ingresar nuevos productos al inventario.
- **Buscar producto:** Búsqueda de producto por nombre.
- **Registrar venta:** Selecciona productos, cantidades y descuenta stock automáticamente.
- **Reportes automáticos:**
  - Histórico: Producto más vendido y total de ventas.
  - Por mes: Reporte de ventas y producto más vendido en un año y mes específico.
  - Entre fechas: Reporte de ventas y producto más vendido en un rango de fechas.
- **Manejo de errores:** Validación de entradas, control de stock y mensajes personalizados.
- **Persistencia:** Los productos se almacenan en un archivo CSV y las ventas en un archivo JSON.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Módulos estándar:**  
  - `csv`  
  - `json`  
  - `datetime`  
  - `uuid`  
  - `collections.Counter`
- **Visual Studio Code**

---

## 📁 Estructura del proyecto

```
LiamStock/
│
├── main.py              # Menú principal e interacción con el usuario
├── models.py            # Clases Producto y Venta
├── database.py          # Funciones para manipular productos y ventas
├── reportes.py          # Funciones para generar reportes
├── productos.csv        # Archivo de productos (inventario)
├── ventas.json          # Archivo de ventas
├── .gitignore           # Archivos y carpetas ignoradas por git
└── README.md            # Documentación del proyecto
```

## 📦 Menú:
![image](https://github.com/user-attachments/assets/b67f6d53-dd44-4932-8364-2bea806de4c2)
---
Ingresar Producto

![image](https://github.com/user-attachments/assets/b76536b4-ad54-4d99-94be-be8a7c74bc0a)

![image](https://github.com/user-attachments/assets/a3598a06-7463-43c4-9c08-b246b82a13ca)
---
Buscar Producto

![image](https://github.com/user-attachments/assets/a008c6ac-63ce-462f-9b9a-1e08716585aa)
---
Menú para registrar venta

![image](https://github.com/user-attachments/assets/1a2bd2a1-a468-4272-bda2-3f7117a90eab)
---
![image](https://github.com/user-attachments/assets/ee5b7278-5c63-4f50-bab0-811e31998842)

Puedes agregar más productos

![image](https://github.com/user-attachments/assets/15de0fef-5606-4104-8119-7e2f326b56ed)
---
Terminar Venta

![image](https://github.com/user-attachments/assets/5b80a1c3-aa1e-4387-8dbd-0aa4dcdd3f53)
---
Resgistro de la venta en JSON

![image](https://github.com/user-attachments/assets/2fe28281-bb63-4179-9f7f-02973c1d83a3)
----
Se descuenta el Stock vendido al terminar la venta

![image](https://github.com/user-attachments/assets/3814549e-f5f8-4454-a8c6-c5bb56cb330b)
---
Menú para generar Reportes

![image](https://github.com/user-attachments/assets/ddf2db84-f4ea-44c7-bafe-fae14de23642)
---
Reporte Historico

![image](https://github.com/user-attachments/assets/3d52da25-f6aa-401b-b26f-5f95817aac7c)

---
Filtrar reporte por mes

![image](https://github.com/user-attachments/assets/5ab04d71-6338-4f9e-a590-20a117d982e7)
---
Filtrar reporte entre fechas

![image](https://github.com/user-attachments/assets/1f2b13b1-badf-4a88-9939-ac5032eff513)

---

## **Contacto**

- 📧 nibaldoji306@gmail.com
- 🌐 [Mi LinkedIn](https://www.linkedin.com/)

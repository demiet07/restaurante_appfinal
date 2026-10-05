# Restaurante App - Semana 16: Manejo de Eventos en Tkinter

## 1. Propósito de la Semana 16
Esta entrega evoluciona el sistema **Restaurante App**, agregando manejo de eventos interactivos en la interfaz gráfica con `Tkinter`. Se implementa la gestión integral de usuarios (CRUD) con control de acceso según roles (`Administrador`, `Empleado`, `Cliente`), vinculando eventos de entrada de ratón, teclado y widgets mediante `bind()` hacia sus respectivos *callbacks*.

---

## 2. Evolución del Proyecto
- **Rol en el Modelo**: Se incorporó el atributo `rol` a la entidad `Usuario`.
- **Restricción por Rol**: La pestaña de usuarios se habilita únicamente para usuarios con rol `Administrador`.
- **Vínculo por Eventos**: Uso de `bind()` para sincronizar las interacciones de selección y atajos de teclado sin sobrecargar el diseño visual.
- **Seguridad en Tablas**: El `Treeview` omite la contraseña visual y la consulta completa se realiza pasando el `id_usuario` a `RestauranteServicio`.

---

## 3. Estructura del Proyecto
```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   └── icon_app.ico
├── main.py
└── README.md
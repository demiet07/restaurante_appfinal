from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.archivo_servicio = ArchivoServicio()
        self.ruta_usuarios = "datos/usuarios.json"
        self.ruta_productos = "datos/productos.json"
        self.ruta_ventas = "datos/ventas.json"

    # --- AUTENTICACIÓN ---
    def autenticar_usuario(self, usuario, clave):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.usuario == usuario and u.clave == clave:
                return u
        return None

    # --- GESTIÓN DE USUARIOS ---
    def obtener_usuarios(self):
        datos = self.archivo_servicio.cargar_json(self.ruta_usuarios)
        return [Usuario.from_dict(item) for item in datos]

    def guardar_usuarios(self, usuarios):
        datos = [u.to_dict() for u in usuarios]
        self.archivo_servicio.guardar_json(self.ruta_usuarios, datos)

    def buscar_usuario_por_id(self, id_usuario):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.id_usuario == str(id_usuario):
                return u
        return None

    def registrar_usuario(self, nombre, usuario, clave, rol):
        if not nombre or not usuario or not clave:
            raise ValueError("Todos los campos (Nombre, Usuario, Clave) son obligatorios.")

        usuarios = self.obtener_usuarios()
        if any(u.usuario.lower() == usuario.lower() for u in usuarios):
            raise ValueError(f"El nombre de usuario '{usuario}' ya existe.")

        nuevo_id = str(max([int(u.id_usuario) for u in usuarios], default=0) + 1)
        nuevo_usuario = Usuario(nuevo_id, nombre, usuario, clave, rol)
        usuarios.append(nuevo_usuario)
        self.guardar_usuarios(usuarios)
        return nuevo_usuario

    def actualizar_usuario(self, id_usuario, nombre, usuario, clave, rol):
        if not nombre or not usuario:
            raise ValueError("Nombre y Usuario son obligatorios.")

        usuarios = self.obtener_usuarios()
        encontrado = False

        for u in usuarios:
            if u.id_usuario == str(id_usuario):
                # Verificar duplicado de nombre de usuario en otra cuenta
                if any(other.usuario.lower() == usuario.lower() and other.id_usuario != str(id_usuario) for other in usuarios):
                    raise ValueError(f"El nombre de usuario '{usuario}' ya está en uso por otra cuenta.")
                
                u.nombre = nombre
                u.usuario = usuario
                if clave.strip():
                    u.clave = clave
                u.rol = rol
                encontrado = True
                break

        if not encontrado:
            raise ValueError("No se encontró el usuario a actualizar.")

        self.guardar_usuarios(usuarios)

    def eliminar_usuario(self, id_usuario, usuario_actual_id):
        if str(id_usuario) == str(usuario_actual_id):
            raise ValueError("No puede eliminar la cuenta con la que inició sesión actualmente.")

        usuarios = self.obtener_usuarios()
        usuarios_filtrados = [u for u in usuarios if u.id_usuario != str(id_usuario)]

        if len(usuarios) == len(usuarios_filtrados):
            raise ValueError("El usuario a eliminar no existe.")

        self.guardar_usuarios(usuarios_filtrados)

    # --- MÉTODOS AUXILIARES PRODUCTOS Y VENTAS ---
    def obtener_productos(self):
        datos = self.archivo_servicio.cargar_json(self.ruta_productos)
        return [Producto.from_dict(item) for item in datos]

    def obtener_ventas(self):
        datos = self.archivo_servicio.cargar_json(self.ruta_ventas)
        return [Venta.from_dict(item) for item in datos]
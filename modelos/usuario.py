class Usuario:
    def __init__(self, id_usuario, nombre, usuario, clave, rol="Cliente"):
        self.id_usuario = str(id_usuario)
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.rol = rol  # 'Administrador', 'Empleado' o 'Cliente'

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "clave": self.clave,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            id_usuario=data.get("id_usuario"),
            nombre=data.get("nombre"),
            usuario=data.get("usuario"),
            clave=data.get("clave"),
            rol=data.get("rol", "Cliente")
        )
class Venta:
    def __init__(self, id_venta, usuario_id, productos, total):
        self.id_venta = str(id_venta)
        self.usuario_id = str(usuario_id)
        self.productos = productos  # Lista de ítems
        self.total = float(total)

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "productos": self.productos,
            "total": self.total
        }

    @staticmethod
    def from_dict(data):
        return Venta(
            id_venta=data.get("id_venta"),
            usuario_id=data.get("usuario_id"),
            productos=data.get("productos", []),
            total=data.get("total", 0.0)
        )
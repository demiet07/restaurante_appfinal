import os
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView

def main():
    # Creación automática de directorios necesarios
    os.makedirs("datos", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    # Inicialización del servicio y la vista de login
    servicio = RestauranteServicio()
    app = LoginView(servicio=servicio)
    app.mainloop()

if __name__ == "__main__":
    main()
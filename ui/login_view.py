import tkinter as tk
from tkinter import ttk, messagebox
from ui.main_view import MainView

class LoginView(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self.title("Restaurante App - Inicio de Sesión")
        self.geometry("380x280")
        self.resizable(False, False)

        try:
            self.iconbitmap("assets/icon_app.ico")
        except Exception:
            pass

        self.crear_interfaz()

    def crear_interfaz(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        lbl_titulo = ttk.Label(frame, text="Acceso al Sistema", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=(0, 15))

        ttk.Label(frame, text="Usuario:").pack(anchor="w", pady=(5, 2))
        self.txt_usuario = ttk.Entry(frame, width=30)
        self.txt_usuario.pack(fill="x", pady=(0, 10))
        self.txt_usuario.focus()

        ttk.Label(frame, text="Contraseña:").pack(anchor="w", pady=(5, 2))
        self.txt_clave = ttk.Entry(frame, show="*", width=30)
        self.txt_clave.pack(fill="x", pady=(0, 15))

        btn_login = ttk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion)
        btn_login.pack(fill="x", ipady=3)

        # Evento Enter para iniciar sesión rápido
        self.bind("<Return>", lambda e: self.iniciar_sesion())

    def iniciar_sesion(self):
        usuario = self.txt_usuario.get().strip()
        clave = self.txt_clave.get().strip()

        if not usuario or not clave:
            messagebox.showwarning("Campos incompletos", "Por favor ingrese su usuario y contraseña.")
            return

        usuario_autenticado = self.servicio.autenticar_usuario(usuario, clave)
        if usuario_autenticado:
            self.destroy()
            app = MainView(usuario_autenticado=usuario_autenticado, servicio=self.servicio)
            app.mainloop()
        else:
            messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
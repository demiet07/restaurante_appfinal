import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Tk):
    def __init__(self, usuario_autenticado, servicio):
        super().__init__()
        self.usuario_actual = usuario_autenticado
        self.servicio = servicio

        self.title(f"Restaurante App - Usuario: {self.usuario_actual.nombre} ({self.usuario_actual.rol})")
        self.geometry("920x620")

        try:
            self.iconbitmap("assets/icon_app.ico")
        except Exception:
            pass

        self.crear_interfaz()

    def crear_interfaz(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Control de acceso por Rol: Solo el Administrador puede gestionar usuarios
        if self.usuario_actual.rol == "Administrador":
            self.tab_usuarios = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_usuarios, text="Gestión de Usuarios")
            self.construir_modulo_usuarios(self.tab_usuarios)

        # Módulos informativos adicionales para el sistema
        self.tab_productos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_productos, text="Catálogo de Productos")
        self.construir_modulo_productos(self.tab_productos)

        self.tab_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ventas, text="Registro de Ventas")
        self.construir_modulo_ventas(self.tab_ventas)

    def construir_modulo_usuarios(self, parent):
        # Frame Formulario
        frame_form = ttk.LabelFrame(parent, text="Formulario de Usuario", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_id = ttk.Entry(frame_form, state="readonly", width=10)
        self.txt_id.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.txt_nombre = ttk.Entry(frame_form, width=25)
        self.txt_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(frame_form, text="Usuario:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_usuario = ttk.Entry(frame_form, width=20)
        self.txt_usuario.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_form, text="Clave:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.txt_clave = ttk.Entry(frame_form, show="*", width=25)
        self.txt_clave.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(frame_form, text="Rol:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_rol = ttk.Combobox(
            frame_form,
            values=["Administrador", "Empleado", "Cliente"],
            state="readonly",
            width=18
        )
        self.combo_rol.set("Empleado")
        self.combo_rol.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.lbl_info_rol = ttk.Label(frame_form, text="Rol seleccionado: Empleado", font=("Arial", 9, "italic"))
        self.lbl_info_rol.grid(row=2, column=2, columnspan=2, sticky="w", padx=5)

        # Frame Botones
        frame_botones = ttk.Frame(parent, padding=5)
        frame_botones.pack(fill="x", padx=10, pady=5)

        btn_registrar = ttk.Button(frame_botones, text="Registrar", command=self.btn_registrar_click)
        btn_registrar.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self.btn_actualizar_click)
        btn_actualizar.pack(side="left", padx=5)

        btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=self.btn_eliminar_click)
        btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = ttk.Button(frame_botones, text="Limpiar (Esc)", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)

        # Frame Tabla Treeview
        frame_tabla = ttk.LabelFrame(parent, text="Listado de Usuarios Registrados", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("id", "nombre", "usuario", "rol")
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        self.tree_usuarios.heading("id", text="ID")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("usuario", text="Nombre de Usuario")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=60, anchor="center")
        self.tree_usuarios.column("nombre", width=220)
        self.tree_usuarios.column("usuario", width=160)
        self.tree_usuarios.column("rol", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscroll=scrollbar.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- EVENTOS MEDIANTE BIND() ---
        # 1. Evento Virtual Treeview: Carga datos de la fila seleccionada
        self.tree_usuarios.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # 2. Evento Virtual Combobox: Cambio de rol en el combo
        self.combo_rol.bind("<<ComboboxSelected>>", self.on_combobox_change)

        # 3. Evento de Teclado: Atajo Enter para registrar
        self.bind("<Return>", self.on_key_return)

        # 4. Evento de Teclado: Atajo Escape para limpiar
        self.bind("<Escape>", self.on_key_escape)

        self.cargar_usuarios_treeview()

    # --- CALLBACKS DE EVENTOS Y ACCIONES ---

    def cargar_usuarios_treeview(self):
        for fila in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(fila)

        usuarios = self.servicio.obtener_usuarios()
        for u in usuarios:
            # No se muestra la clave por motivos de seguridad
            self.tree_usuarios.insert("", "end", iid=u.id_usuario, values=(u.id_usuario, u.nombre, u.usuario, u.rol))

    def on_treeview_select(self, event):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return

        id_usuario = seleccion[0]
        usuario = self.servicio.buscar_usuario_por_id(id_usuario)

        if usuario:
            self.txt_id.config(state="normal")
            self.txt_id.delete(0, tk.END)
            self.txt_id.insert(0, usuario.id_usuario)
            self.txt_id.config(state="readonly")

            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, usuario.nombre)

            self.txt_usuario.delete(0, tk.END)
            self.txt_usuario.insert(0, usuario.usuario)

            self.txt_clave.delete(0, tk.END)
            self.txt_clave.insert(0, usuario.clave)

            self.combo_rol.set(usuario.rol)
            self.on_combobox_change(None)

    def on_combobox_change(self, event):
        rol_seleccionado = self.combo_rol.get()
        self.lbl_info_rol.config(text=f"Rol seleccionado: {rol_seleccionado}")

    def on_key_return(self, event):
        # Reutiliza el callback de registrar
        self.btn_registrar_click()

    def on_key_escape(self, event):
        # Reutiliza el callback de limpiar
        self.limpiar_formulario()

    def btn_registrar_click(self):
        try:
            nombre = self.txt_nombre.get().strip()
            usuario = self.txt_usuario.get().strip()
            clave = self.txt_clave.get().strip()
            rol = self.combo_rol.get()

            self.servicio.registrar_usuario(nombre, usuario, clave, rol)
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.cargar_usuarios_treeview()
            self.limpiar_formulario()
        except ValueError as err:
            messagebox.showwarning("Atención", str(err))

    def btn_actualizar_click(self):
        id_usuario = self.txt_id.get().strip()
        if not id_usuario:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para actualizar.")
            return

        try:
            nombre = self.txt_nombre.get().strip()
            usuario = self.txt_usuario.get().strip()
            clave = self.txt_clave.get().strip()
            rol = self.combo_rol.get()

            self.servicio.actualizar_usuario(id_usuario, nombre, usuario, clave, rol)
            messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
            self.cargar_usuarios_treeview()
            self.limpiar_formulario()
        except ValueError as err:
            messagebox.showwarning("Atención", str(err))

    def btn_eliminar_click(self):
        id_usuario = self.txt_id.get().strip()
        if not id_usuario:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar el usuario seleccionado?")
        if confirmacion:
            try:
                self.servicio.eliminar_usuario(id_usuario, self.usuario_actual.id_usuario)
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                self.cargar_usuarios_treeview()
                self.limpiar_formulario()
            except ValueError as err:
                messagebox.showerror("Error", str(err))

    def limpiar_formulario(self):
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")

        self.txt_nombre.delete(0, tk.END)
        self.txt_usuario.delete(0, tk.END)
        self.txt_clave.delete(0, tk.END)
        self.combo_rol.set("Empleado")
        self.on_combobox_change(None)

        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

    # --- MÓDULOS DE COMPLEMENTO ---
    def construir_modulo_productos(self, parent):
        lbl = ttk.Label(parent, text="Lista de Productos Disponibles", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        tree = ttk.Treeview(parent, columns=("id", "nombre", "precio", "stock"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Producto")
        tree.heading("precio", text="Precio ($)")
        tree.heading("stock", text="Stock")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for p in self.servicio.obtener_productos():
            tree.insert("", "end", values=(p.id_producto, p.nombre, f"${p.precio:,.0f}", p.stock))

    def construir_modulo_ventas(self, parent):
        lbl = ttk.Label(parent, text="Historial de Ventas Registradas", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        tree = ttk.Treeview(parent, columns=("id", "usuario", "total"), show="headings")
        tree.heading("id", text="ID Venta")
        tree.heading("usuario", text="ID Usuario")
        tree.heading("total", text="Total ($)")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for v in self.servicio.obtener_ventas():
            tree.insert("", "end", values=(v.id_venta, v.usuario_id, f"${v.total:,.0f}"))
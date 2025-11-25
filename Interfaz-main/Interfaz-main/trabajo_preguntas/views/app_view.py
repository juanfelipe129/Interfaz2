import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os

class FormularioVista:

    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Registro de Empleados")
        self.root.iconbitmap(r"C:\Users\RSP-L16-LT-003\Documents\Interfaz-main\Interfaz-main\Interfaz-main\icono.ico")
        self.root.state("zoomed")

        self.foto_path = None
        self.imagen_preview = None

        self.construir_ui()

    def construir_ui(self):
        # ----------- TITULO Y BOTONES SUPERIORES -----------
        titulo_frame = tk.Frame(self.root, bg="#003566")
        titulo_frame.pack(fill="x")
        tk.Label(titulo_frame, text="REGISTRO DE EMPLEADOS",
                 font=("Segoe UI", 20, "bold"), fg="white", bg="#003566", pady=10).pack(side="left", padx=20)

        botones_top = tk.Frame(titulo_frame, bg="#003566")
        botones_top.pack(side="right", padx=20)

        tk.Button(botones_top, text="Buscar", command=self.ventana_buscar).pack(side="left", padx=10)
        tk.Button(botones_top, text="Ayuda", command=self.ventana_ayuda).pack(side="left", padx=10)
        tk.Button(botones_top, text="Créditos", command=self.ventana_creditos).pack(side="left", padx=10)

        # ----------- FORMULARIO -----------
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.entry_nombre = tk.Entry(form_frame, width=40)
        self.entry_nombre.grid(row=0, column=1)
        self.entry_nombre.bind("<FocusOut>", self.capitalizar_iniciales)

        tk.Label(form_frame, text="Empresa:").grid(row=1, column=0, sticky="e")
        self.entry_empresa = tk.Entry(form_frame, width=40)
        self.entry_empresa.grid(row=1, column=1)

        tk.Label(form_frame, text="Cargo:").grid(row=2, column=0, sticky="e")
        self.entry_cargo = tk.Entry(form_frame, width=40)
        self.entry_cargo.grid(row=2, column=1)

        tk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="e")
        self.entry_telefono = tk.Entry(form_frame, width=40)
        self.entry_telefono.grid(row=3, column=1)

        tk.Label(form_frame, text="Correo:").grid(row=4, column=0, sticky="e")
        self.entry_correo = tk.Entry(form_frame, width=40)
        self.entry_correo.grid(row=4, column=1)

        tk.Label(form_frame, text="Ciudad:").grid(row=5, column=0, sticky="e")
        self.entry_ciudad = tk.Entry(form_frame, width=40)
        self.entry_ciudad.grid(row=5, column=1)

        tk.Label(form_frame, text="Fecha Nacimiento:").grid(row=6, column=0, sticky="e")
        self.entry_fecha = DateEntry(form_frame, width=15, date_pattern="dd/mm/yyyy")
        self.entry_fecha.grid(row=6, column=1, sticky="w")

        tk.Label(form_frame, text="Número de Hijos:").grid(row=7, column=0, sticky="e")
        self.spin_hijos = tk.Spinbox(form_frame, from_=0, to=20, width=5)
        self.spin_hijos.grid(row=7, column=1, sticky="w")

        tk.Label(form_frame, text="Foto (opcional):").grid(row=8, column=0, sticky="e")
        tk.Button(form_frame, text="Seleccionar archivo", command=self.cargar_foto).grid(row=8, column=1, sticky="w")

        tk.Button(form_frame, text="Registrar", bg="#003566", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.registrar).grid(row=9, column=0, columnspan=2, pady=10)

        # ----------- TABLA INFERIOR -----------
        tabla_frame = tk.Frame(self.root)
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("nombre", "empresa", "cargo", "telefono", "correo", "ciudad", "hijos", "fecha")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, anchor="center", width=150)

        self.tabla.pack(fill="both", expand=True)

        try:
            self.actualizar_tabla(self.controlador.obtener_empresarios())
        except Exception:
            try:
                self.actualizar_tabla(self.controlador.empresarios)
            except Exception:
                pass

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_empresa.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_ciudad.delete(0, tk.END)

        try:
            self.entry_fecha.set_date("")
        except:
            pass

        self.spin_hijos.delete(0, tk.END)
        self.spin_hijos.insert(0, 0)

        self.foto_path = None
        self.imagen_preview = None
        
    # =======================================================
    #                   FUNCIONES BÁSICAS
    # =======================================================

    def capitalizar_iniciales(self, event=None):
        texto = self.entry_nombre.get().strip()
        if texto:
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, " ".join([p.capitalize() for p in texto.split()]))

    def cargar_foto(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
        )
        if ruta:
            self.foto_path = ruta
            try:
                img = Image.open(ruta).resize((120,120))
                self.imagen_preview = ImageTk.PhotoImage(img)
            except Exception:
                pass

    def registrar(self):
        datos = {
            "nombre": self.entry_nombre.get().strip(),
            "empresa": self.entry_empresa.get().strip(),
            "cargo": self.entry_cargo.get().strip(),
            "telefono": self.entry_telefono.get().strip(),
            "correo": self.entry_correo.get().strip(),
            "ciudad": self.entry_ciudad.get().strip(),
            "fecha de nacimiento": self.entry_fecha.get(),
            "n° de hijos": int(self.spin_hijos.get()),
            "foto": self.foto_path or ""
        }

        # Registrar en el controlador
        self.controlador.registrar_empresario(datos)

        # Actualizar tabla
        self.actualizar_tabla(self.controlador.obtener_empresarios())

        
        self.limpiar_formulario()

        messagebox.showinfo("Registro", "Empleado registrado correctamente.")

    def actualizar_tabla(self, lista):
        self.tabla.delete(*self.tabla.get_children())
        for idx, e in enumerate(lista):
            self.tabla.insert("", tk.END, iid=str(idx), values=(
                e.get("nombre", ""),
                e.get("empresa", ""),
                e.get("cargo", ""),
                e.get("telefono", ""),
                e.get("correo", ""),
                e.get("ciudad", ""),
                e.get("n° de hijos", 0),
                e.get("fecha de nacimiento", "")
            ))


    # =======================================================
    #                   VENTANA DE BÚSQUEDA
    # =======================================================

    def ventana_buscar(self):
        win = tk.Toplevel(self.root)
        win.title("Buscar Empleados")
        win.geometry("1220x600")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Buscar por nombre o empresa:").pack(pady=10)
        entry_buscar = tk.Entry(win, width=45)
        entry_buscar.pack()

        main_frame = tk.Frame(win)
        main_frame.pack(fill="both", expand=True)

        columnas = ("nombre", "empresa", "cargo", "telefono", "correo", "ciudad", "hijos", "fecha")
        tabla = ttk.Treeview(main_frame, columns=columnas, show="headings")
        tabla.pack(side="left", fill="both", expand=True)

        for col in columnas:
            tabla.heading(col, text=col.capitalize())
            tabla.column(col, width=120, anchor="center")

        panel = tk.Frame(main_frame, padx=20, pady=20)
        panel.pack(side="right", fill="y")

        label_imagen = tk.Label(panel)
        label_imagen.pack()

        label_info = tk.Label(panel, justify="left", font=("Segoe UI", 10), anchor="nw")
        label_info.pack(pady=10)

        # --- cargar todos los registros ---
        def cargar_todos():
            tabla.delete(*tabla.get_children())
            empresarios = self.controlador.obtener_empresarios()
            for idx, e in enumerate(empresarios):
                tabla.insert("", tk.END, iid=str(idx), values=(
                    e.get("nombre", ""),
                    e.get("empresa", ""),
                    e.get("cargo", ""),
                    e.get("telefono", ""),
                    e.get("correo", ""),
                    e.get("ciudad", ""),
                    e.get("n° de hijos", 0),
                    e.get("fecha de nacimiento", "")
                ))

        cargar_todos()

        # --- mostrar detalles de la fila seleccionada ---
        def mostrar_detalles(event=None):
            sel = tabla.selection()
            if not sel:
                return

            iid = sel[0]
            try:
                idx = int(iid)
            except Exception:
                return

            empresarios = self.controlador.obtener_empresarios()
            if idx >= len(empresarios):
                return

            datos = empresarios[idx]

            info = (
                f"Nombre: {datos.get('nombre','')}\n"
                f"Empresa: {datos.get('empresa','')}\n"
                f"Cargo: {datos.get('cargo','')}\n"
                f"Teléfono: {datos.get('telefono','')}\n"
                f"Correo: {datos.get('correo','')}\n"
                f"Ciudad: {datos.get('ciudad','')}\n"
                f"Hijos: {datos.get('n° de hijos',0)}\n"
                f"Fecha: {datos.get('fecha de nacimiento','')}"
            )
            label_info.config(text=info)

            foto_path = datos.get("foto", "")
            if foto_path and os.path.exists(foto_path):
                try:
                    img = Image.open(foto_path)
                    img = img.resize((180, 180))
                    photo = ImageTk.PhotoImage(img)

                    win.foto_img = photo
                    label_imagen.photo = photo
                    label_imagen.config(image=photo, text="")
                except Exception:
                    win.foto_img = None
                    label_imagen.config(image="", text="Error al cargar imagen")
            else:
                win.foto_img = None
                label_imagen.config(image="", text="Sin foto")

        tabla.bind("<<TreeviewSelect>>", mostrar_detalles)

        # --- ejecutar búsqueda ---
        def ejecutar_busqueda():
            termino = entry_buscar.get().strip().lower()
            tabla.delete(*tabla.get_children())

            empresarios = self.controlador.obtener_empresarios()

            for idx, e in enumerate(empresarios):
                if termino in e.get("nombre","").lower() or termino in e.get("empresa","").lower():
                    tabla.insert("", tk.END, iid=str(idx), values=(
                        e.get("nombre",""),
                        e.get("empresa",""),
                        e.get("cargo",""),
                        e.get("telefono",""),
                        e.get("correo",""),
                        e.get("ciudad",""),
                        e.get("n° de hijos",0),
                        e.get("fecha de nacimiento","")
                    ))

            if not tabla.get_children():
                cargar_todos()

        tk.Button(win, text="Buscar", command=ejecutar_busqueda).pack(pady=10)

        # =======================================================
        #                   ELIMINAR REGISTRO
        # =======================================================

        def eliminar_sel():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Seleccione", "Seleccione un registro.")
                return

            try:
                idx = int(sel[0])
            except Exception:
                return

            empresarios = self.controlador.obtener_empresarios()
            if idx < 0 or idx >= len(empresarios):
                return

            nombre = empresarios[idx].get("nombre","")

            if messagebox.askyesno("Confirmar", f"¿Eliminar {nombre}?"):
                try:
                    self.controlador.eliminar_empresario(nombre)
                except AttributeError:
                    self.controlador.eliminar(nombre)

                cargar_todos()
                label_imagen.config(image="", text="")
                label_info.config(text="")

        tk.Button(win, text="Eliminar", bg="red", fg="white", command=eliminar_sel).pack(pady=5)

        # =======================================================
        #                   MODIFICAR REGISTRO
        # =======================================================

        def modificar_sel():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Seleccione", "Seleccione un registro.")
                return

            try:
                idx = int(sel[0])
            except Exception:
                return

            empresarios = self.controlador.obtener_empresarios()
            if idx < 0 or idx >= len(empresarios):
                return

            datos = empresarios[idx]
            self.ventana_modificar(datos, cargar_todos)

        tk.Button(win, text="Modificar", bg="#003566", fg="white", command=modificar_sel).pack(pady=5)

    # =======================================================
    #                   VENTANA MODIFICAR 
    # =======================================================

    def ventana_modificar(self, datos, refrescar_callback):
        win = tk.Toplevel(self.root)
        win.title("Modificar Empleado")
        win.geometry("520x620")
        win.transient(self.root)
        win.grab_set()

        foto_original = datos.get("foto", "")

        labels = [
            ("nombre", "Nombre"),
            ("empresa", "Empresa"),
            ("cargo", "Cargo"),
            ("telefono", "Teléfono"),
            ("correo", "Correo"),
            ("ciudad", "Ciudad"),
            ("n° de hijos", "N° de hijos"),
            ("fecha de nacimiento", "Fecha de nacimiento"),
        ]

        entries = {}

        for i, (key, label_text) in enumerate(labels):
            tk.Label(win, text=label_text + ":").grid(row=i, column=0, sticky="e", padx=8, pady=6)
            ent = tk.Entry(win, width=35)
            ent.grid(row=i, column=1, padx=8, pady=6)
            ent.insert(0, "" if datos.get(key) is None else str(datos.get(key)))
            entries[key] = ent

        entries["nombre"].focus_set()

        tk.Label(win, text="Foto (opcional):").grid(row=len(labels), column=0, sticky="e", padx=8, pady=6)
        foto_label = tk.Label(win, text=os.path.basename(foto_original) if foto_original else "Sin foto")
        foto_label.grid(row=len(labels), column=1, sticky="w", padx=8, pady=6)

        def cambiar_foto():
            ruta = filedialog.askopenfilename(
                title="Seleccionar imagen",
                filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")]
            )
            if ruta:
                entries["foto_nueva"] = ruta
                foto_label.config(text=os.path.basename(ruta))

        tk.Button(win, text="Cambiar foto", command=cambiar_foto).grid(row=len(labels)+1, column=0, columnspan=2, pady=8)

        def guardar_modificacion():
            nuevos = {}
            for key, _ in labels:
                v = entries[key].get().strip()
                if key == "n° de hijos":
                    try:
                        nuevos[key] = int(v) if v != "" else 0
                    except:
                        messagebox.showerror("Error", "El campo 'N° de hijos' debe ser un número entero.")
                        entries[key].focus_set()
                        return
                else:
                    nuevos[key] = v

            nuevos["foto"] = entries.get("foto_nueva", foto_original)

            nombre_original = datos.get("nombre", "")

            try:
                self.controlador.modificar_empresario(nombre_original, nuevos)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar: {e}")
                return

            try:
                refrescar_callback()
            except:
                pass

            try:
                self.actualizar_tabla(self.controlador.obtener_empresarios())
            except:
                pass

            win.destroy()
            messagebox.showinfo("Éxito", "Cambios guardados correctamente.")

        tk.Button(win, text="Guardar Cambios", bg="#003566", fg="white",
                  command=guardar_modificacion).grid(row=len(labels)+2, column=0, columnspan=2, pady=12)

    # =======================================================
    #                   AYUDA / CRÉDITOS
    # =======================================================

    def ventana_ayuda(self):
        messagebox.showinfo("Ayuda", "Pon los datos del empleado y dale al botón de registrar.")
        
    def ventana_creditos(self):
        messagebox.showinfo("Créditos", "Desarrollado por Juan Felipe Almeciga y Daniel Hernandez.")

import os
import json
from tkinter import messagebox

class FormularioControlador:
    def __init__(self, vista):
        self.vista = vista

        # Ruta fija al JSON dentro de /views/
        self.archivo_json = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "views", "empresarios.json")
        )

        # Crear archivo si no existe
        carpeta = os.path.dirname(self.archivo_json)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

        if not os.path.exists(self.archivo_json):
            with open(self.archivo_json, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

        self.empresarios = self.obtener_empresarios()

        # Conectar vista → controlador
        self.vista.controlador = self
        self.vista.actualizar_tabla(self.empresarios)

    # ----------------------------------------------------------
    # Cargar JSON
    # ----------------------------------------------------------
    def obtener_empresarios(self):
        try:
            with open(self.archivo_json, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos if isinstance(datos, list) else []
        except:
            return []

    # ----------------------------------------------------------
    # Guardar JSON
    # ----------------------------------------------------------
    def guardar_empresarios(self):
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(self.empresarios, f, indent=4, ensure_ascii=False)

    # ----------------------------------------------------------
    # Registrar
    # ----------------------------------------------------------
    def registrar_empresario(self, datos):

        nuevo = {
            "nombre": datos.get("nombre", "").strip(),
            "empresa": datos.get("empresa", "").strip(),
            "cargo": datos.get("cargo", "").strip(),
            "telefono": datos.get("telefono", "").strip(),
            "correo": datos.get("correo", "").strip(),
            "ciudad": datos.get("ciudad", "").strip(),
            "fecha de nacimiento": datos.get("fecha de nacimiento", "").strip(),
            "n° de hijos": datos.get("n° de hijos", 0),
            "foto": datos.get("foto", "") or ""
        }

        if not nuevo["nombre"]:
            messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
            return
        if not nuevo["empresa"]:
            messagebox.showerror("Error", "El campo 'Empresa' es obligatorio.")
            return

        self.empresarios.append(nuevo)
        self.guardar_empresarios()
        self.vista.actualizar_tabla(self.empresarios)

        messagebox.showinfo("Éxito", f"Empresario '{nuevo['nombre']}' registrado correctamente.")

    # ----------------------------------------------------------
    # Buscar
    # ----------------------------------------------------------
    def buscar_empresarios(self, termino):
        termino = termino.lower().strip()

        if termino == "":
            return self.empresarios

        return [
            e for e in self.empresarios
            if termino in e["nombre"].lower() or termino in e["empresa"].lower()
        ]

    # ----------------------------------------------------------
    # Eliminar
    # ----------------------------------------------------------
    def eliminar_empresario(self, nombre):
        self.empresarios = [e for e in self.empresarios if e["nombre"] != nombre]
        self.guardar_empresarios()
        self.vista.actualizar_tabla(self.empresarios)
        messagebox.showinfo("Eliminado", f"El empresario '{nombre}' fue eliminado.")

    # ----------------------------------------------------------
    # Modificar
    # ----------------------------------------------------------
    def modificar_empresario(self, nombre_original, datos_nuevos):

        for e in self.empresarios:
            if e["nombre"] == nombre_original:
                e.update({
                    "nombre": datos_nuevos.get("nombre", e["nombre"]),
                    "empresa": datos_nuevos.get("empresa", e["empresa"]),
                    "cargo": datos_nuevos.get("cargo", e["cargo"]),
                    "telefono": datos_nuevos.get("telefono", e["telefono"]),
                    "correo": datos_nuevos.get("correo", e["correo"]),
                    "ciudad": datos_nuevos.get("ciudad", e["ciudad"]),
                    "fecha de nacimiento": datos_nuevos.get("fecha de nacimiento", e["fecha de nacimiento"]),
                    "n° de hijos": datos_nuevos.get("n° de hijos", e["n° de hijos"]),
                    "foto": datos_nuevos.get("foto", e["foto"]),
                })
                break

        self.guardar_empresarios()
        self.vista.actualizar_tabla(self.empresarios)
        messagebox.showinfo("Modificado", f"Datos de '{nombre_original}' modificados correctamente.")

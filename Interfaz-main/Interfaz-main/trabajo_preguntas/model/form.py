import json

class FormularioModelo:
    def __init__(self):
        self.datos = {}

    def guardar_datos(self, nombre, correo, fecha, telefono, empresa, hijos):
        self.datos = {
            "Nombre": nombre,
            "Correo": correo,
            "Fecha de nacimiento": fecha,
            "Teléfono": telefono,
            "Empresa": empresa,
            "Hijos": hijos
        }

    def obtener_datos(self):
        return self.datos

    def cargar_json(self, ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def buscar_json(self, campo, valor):
        with open("views/empresarios.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return [emp for emp in data if str(emp.get(campo, "")).lower() == valor.lower()]





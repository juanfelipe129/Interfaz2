from controller.controller import FormularioControlador
from views.app_view import FormularioVista
import tkinter as tk

root = tk.Tk()

# Se crea el controlador después de la vista
vista = FormularioVista(root, None)
controlador = FormularioControlador(vista)
vista.controlador = controlador

root.mainloop()


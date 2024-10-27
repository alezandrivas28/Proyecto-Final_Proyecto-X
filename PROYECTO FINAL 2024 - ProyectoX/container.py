from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import ControlClientes
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.config(bg="#d3d3d3")  # Fondo gris claro para todo el container
        self.place(x=0, y=0, width=800, height=400)
        self.crear_widgets()

    def show_frames(self, container):
        """Abre una nueva ventana con el frame seleccionado."""
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#d3d3d3")  # Fondo gris claro para los frames internos
        frame.pack(fill="both", expand=True)

        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(ControlClientes)

    def crear_widgets(self):
        """Crea los botones y elementos visuales."""
        frame1 = tk.Frame(self, bg="#b0b0b0")  # Fondo gris medio
        frame1.place(x=0, y=0, width=800, height=400)

        btn_ventas = Button(
            frame1, text="Ir a Ventas", font="sans 18 bold",
            bg="#a0a0a0", fg="black", command=self.ventas
        )
        btn_ventas.place(x=500, y=30, width=240, height=60)

        btn_inventario = Button(
            frame1, text="Ir a Inventario", font="sans 18 bold",
            bg="#909090", fg="black", command=self.inventario
        )
        btn_inventario.place(x=500, y=130, width=240, height=60)

        btn_clientes = Button(
            frame1, text="Ir a Clientes", font="sans 18 bold",
            bg="#808080", fg="black", command=self.clientes
        )
        btn_clientes.place(x=500, y=230, width=240, height=60)

        # Logo en escala de grises
        self.logo_image = Image.open("imagenes/Logo_gris.jpg").resize((280, 280))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#b0b0b0")
        self.logo_label.place(x=100, y=30)

        # Texto de copyright en blanco sobre fondo gris
        copyright_label = tk.Label(
            frame1, text="© 2024 Proyecto_X Todos los derechos reservados",
            font="sans 12 bold", bg="#b0b0b0", fg="white"
        )
        copyright_label.place(x=180, y=350)

# Ventana principal
def mostrar_menu():
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú Principal")
    ventana_menu.geometry("800x400+120+50")
    ventana_menu.resizable(False, False)

    container = Container(ventana_menu, None)
    ventana_menu.mainloop()

mostrar_menu()

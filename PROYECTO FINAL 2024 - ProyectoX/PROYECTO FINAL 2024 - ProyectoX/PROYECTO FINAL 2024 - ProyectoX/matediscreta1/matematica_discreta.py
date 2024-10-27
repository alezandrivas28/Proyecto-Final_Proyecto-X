import tkinter as tk
from tkinter import *
from math import factorial
from PIL import Image, ImageTk

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.place(x=0, y=0, width=800, height=400)

        self.canvas = tk.Canvas(self, width=800, height=400, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_degradado()
        self.crear_widgets()

    def dibujar_degradado(self):
        """Crea un degradado en escala de grises."""
        for i in range(400):
            color = self.degradado_color(i, 400, "#ffffff", "#000000")
            self.canvas.create_line(0, i, 800, i, fill=color)

    def degradado_color(self, i, total, color1, color2):
        """Calcula el color intermedio en el degradado."""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * i / total)
        g = int(g1 + (g2 - g1) * i / total)
        b = int(b1 + (b2 - b1) * i / total)

        return f"#{r:02x}{g:02x}{b:02x}"

    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#d3d3d3")
        frame.pack(fill="both", expand=True)

        top_level.geometry("600x400+150+50")
        top_level.resizable(False, False)
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()

    def permutaciones(self):
        self.show_frames(Permutaciones)

    def combinaciones(self):
        self.show_frames(Combinaciones)

    def crear_widgets(self):
        """Crea los widgets principales del menú."""
        frame1 = tk.Frame(self, bg="#d3d3d3")
        frame1.place(relx=0.5, rely=0.5, anchor="center", width=700, height=350)

        btn_permutaciones = Button(frame1, text="Ir a Permutaciones", font="sans 16 bold", 
                                   bg="#b0b0b0", command=self.permutaciones)
        btn_permutaciones.place(x=400, y=50, width=240, height=50)

        btn_combinaciones = Button(frame1, text="Ir a Combinaciones", font="sans 16 bold", 
                                   bg="#a0a0a0", command=self.combinaciones)
        btn_combinaciones.place(x=400, y=130, width=240, height=50)

        self.logo_image = Image.open("imagenes/Logo_gris.jpg").resize((200, 200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        logo_label = tk.Label(frame1, image=self.logo_image, bg="#d3d3d3")
        logo_label.place(x=50, y=70)

        copyright_label = tk.Label(frame1, text="© 2024 proyecto_X Todos los derechos reservados",
                                   font="sans 10", bg="#d3d3d3", fg="black")
        copyright_label.place(x=220, y=300)

class Permutaciones(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.config(bg="#d3d3d3")
        self.crear_widgets()

    def crear_widgets(self):
        """Crea los widgets para la vista de Permutaciones."""
        tk.Label(self, text="Cálculo de Permutaciones", font="Arial 18 bold", bg="#d3d3d3").pack(pady=15)

        self.entry_n = self.crear_entrada("Número total de elementos (n):")
        self.entry_r = self.crear_entrada("Número de elementos a seleccionar (r):")

        self.var_repeticion = tk.BooleanVar()
        tk.Checkbutton(self, text="¿Permitir repetición?", variable=self.var_repeticion, bg="#d3d3d3").pack(pady=5)

        tk.Button(self, text="Calcular Permutación", command=self.calcular_permutacion,
                  font="Arial 12 bold", bg="#b0b0b0").pack(pady=15)

        self.result_label = tk.Label(self, text="Resultado:", font="Arial 14 bold", bg="#d3d3d3")
        self.result_label.pack(pady=10)

    def crear_entrada(self, texto):
        """Crea una entrada con su etiqueta correspondiente."""
        tk.Label(self, text=texto, font="Arial 12", bg="#d3d3d3").pack(pady=5)
        entrada = tk.Entry(self, font="Arial 12")
        entrada.pack(pady=5)
        return entrada

    def calcular_permutacion(self):
        """Calcula las permutaciones según los valores ingresados."""
        try:
            n = int(self.entry_n.get())
            r = int(self.entry_r.get())
            resultado = n ** r if self.var_repeticion.get() else factorial(n) // factorial(n - r)
            self.result_label.config(text=f"Resultado: {resultado}")
        except ValueError:
            self.result_label.config(text="Error: Ingrese números válidos.")

class Combinaciones(Permutaciones):
    def calcular_permutacion(self):  
        """Calcula las combinaciones según los valores ingresados."""
        try:
            n = int(self.entry_n.get())
            r = int(self.entry_r.get())
            if self.var_repeticion.get():
                resultado = factorial(n + r - 1) // (factorial(r) * factorial(n - 1))
            else:
                resultado = factorial(n) // (factorial(r) * factorial(n - r))
            self.result_label.config(text=f"Resultado: {resultado}")
        except ValueError:
            self.result_label.config(text="Error: Ingrese números válidos.")

def mostrar_menu():
    ventana_menu = tk.Tk()
    ventana_menu.title("Menú Principal")
    container = Container(ventana_menu, None)
    ventana_menu.geometry("800x400+120+50")
    ventana_menu.resizable(False, False)
    ventana_menu.mainloop()

mostrar_menu()

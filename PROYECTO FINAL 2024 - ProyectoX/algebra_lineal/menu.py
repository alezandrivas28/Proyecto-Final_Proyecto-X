import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import subprocess
from fractions import Fraction

class MenuPrincipal(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=600, height=400)
        self.config(bg="#3C3C3C")
        self.widgets()

    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#3C3C3C")
        frame.pack(fill="both", expand=True)
        top_level.geometry("800x600+120+20")
        top_level.resizable(False, False)

    def calculadora_multiplicacion(self):
        self.show_frames(MultiplicacionMatricesApp)

    def calculadora_inversa(self):
        self.show_frames(InversaMatrizApp)

    def calculadora_ecuaciones(self):
        try:
            subprocess.run(["python", "algebra_lineal/ecu.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo ecu.py: {e}")
        

    def widgets(self):
        frame = tk.Frame(self, bg="#3C3C3C")
        frame.pack()
        frame.place(x=0, y=0, width=600, height=400)

        btn_multiplicacion = tk.Button(frame, bg="#8c8c8c", fg="black", font="sans 16 bold", text="Multiplicación de Matrices", command=self.calculadora_multiplicacion)
        btn_multiplicacion.place(x=150, y=80, width=300, height=60)

        btn_inversa = tk.Button(frame, bg="#8c8c8c", fg="black", font="sans 16 bold", text="Inversa de Matriz", command=self.calculadora_inversa)
        btn_inversa.place(x=150, y=160, width=300, height=60)

        btn_ecuaciones = tk.Button(frame, bg="#8c8c8c", fg="black", font="sans 16 bold", text="Sistema de Ecuaciones", command=self.calculadora_ecuaciones)
        btn_ecuaciones.place(x=150, y=240, width=300, height=60)

        copyright_label = tk.Label(frame, text="© 2024 PROYECTO X Code. Todos los derechos reservados", font="sans 10 bold", bg="#3C3C3C", fg="white")
        copyright_label.place(x=150, y=320)

class MultiplicacionMatricesApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Multiplicación de Matrices")
        self.root.geometry("800x600")
        self.config(bg="#3C3C3C")
        self.pack()
        self.place(x=0, y=0, width=800, height=600)
        self.widgets()

        self.filas1 = 0
        self.columnas1 = 0
        self.filas2 = 0
        self.columnas2 = 0
        self.entradas_matriz1 = None
        self.entradas_matriz2 = None
        self.result_labels = []

    def widgets(self):
        frame1 = tk.Frame(self, bg="#3C3C3C")
        frame1.place(x=0, y=0, width=800, height=600)

        titulo = tk.Label(frame1, text="Calculadora de Multiplicación de Matrices", font=("Arial", 18, "bold"), bg="#3C3C3C", fg="white")
        titulo.place(x=200, y=20)

        self.btn_crear_matriz1 = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Crear Matriz 1", command=self.crear_matriz1)
        self.btn_crear_matriz1.place(x=500, y=100, width=240, height=60)

        self.btn_crear_matriz2 = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Crear Matriz 2", command=self.crear_matriz2)
        self.btn_crear_matriz2.place(x=500, y=200, width=240, height=60)

        self.btn_multiplicar = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Multiplicar Matrices", state=tk.DISABLED, command=self.multiplicar_matrices)
        self.btn_multiplicar.place(x=500, y=300, width=240, height=60)

        self.result_frame = tk.Frame(frame1, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.result_frame.place(x=100, y=420, width=600, height=150)

        copyright_label = tk.Label(frame1, text="© 2024 PROYECTO X Code. Todos los derechos reservados", font=("Arial", 10), bg="#3C3C3C", fg="white")
        copyright_label.place(x=250, y=570)

        self.matrix_frame = tk.Frame(frame1, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.matrix_frame.place(x=30, y=90, width=450, height=320)

    def crear_matriz1(self):
        try:
            self.filas1 = int(simpledialog.askstring("Entrada", "Número de filas para la Matriz 1:"))
            self.columnas1 = int(simpledialog.askstring("Entrada", "Número de columnas para la Matriz 1:"))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        if self.filas1 <= 0 or self.columnas1 <= 0:
            messagebox.showerror("Error", "Las filas y columnas deben ser números positivos.")
            return

        self.limpiar_entradas_matrices()

        self.entradas_matriz1 = [[tk.Entry(self.matrix_frame, width=5, font=("Arial", 12)) for _ in range(self.columnas1)] for _ in range(self.filas1)]
        for i in range(self.filas1):
            for j in range(self.columnas1):
                self.entradas_matriz1[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.btn_crear_matriz2.config(state=tk.NORMAL)

    def crear_matriz2(self):
        try:
            self.filas2 = int(simpledialog.askstring("Entrada", "Número de filas para la Matriz 2:"))
            self.columnas2 = int(simpledialog.askstring("Entrada", "Número de columnas para la Matriz 2:"))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        if self.filas2 <= 0 or self.columnas2 <= 0:
            messagebox.showerror("Error", "Las filas y columnas deben ser números positivos.")
            return

        self.limpiar_entradas_matrices(clear_matriz1=False)

        self.entradas_matriz2 = [[tk.Entry(self.matrix_frame, width=5, font=("Arial", 12)) for _ in range(self.columnas2)] for _ in range(self.filas2)]
        for i in range(self.filas2):
            for j in range(self.columnas2):
                self.entradas_matriz2[i][j].grid(row=i + self.filas1 + 1, column=j, padx=5, pady=5)

        self.btn_multiplicar.config(state=tk.NORMAL)

    def limpiar_entradas_matrices(self, clear_matriz1=True):
        if clear_matriz1 and self.entradas_matriz1:
            for row in self.entradas_matriz1:
                for entry in row:
                    entry.destroy()
        if self.entradas_matriz2:
            for row in self.entradas_matriz2:
                for entry in row:
                    entry.destroy()

        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

    def obtener_matriz(self, entradas, filas, columnas):
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                try:
                    valor_entrada = float(entradas[i][j].get())
                    fila.append(valor_entrada)
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingresa valores válidos en la matriz.")
                    return None
            matriz.append(fila)
        return np.array(matriz)

    def multiplicar_matrices(self):
        matrix1 = self.obtener_matriz(self.entradas_matriz1, self.filas1, self.columnas1)
        matrix2 = self.obtener_matriz(self.entradas_matriz2, self.filas2, self.columnas2)

        if matrix1 is None or matrix2 is None:
            return

        if self.columnas1 != self.filas2:
            messagebox.showerror("Error", "El número de columnas de la primera matriz debe ser igual al número de filas de la segunda.")
            return

        try:
            resultado = np.dot(matrix1, matrix2)
            self.mostrar_resultado(resultado)
        except Exception as e:
            messagebox.showerror("Error", "No se pudo realizar la multiplicación. " + str(e))

    def mostrar_resultado(self, resultado):
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

        label_resultado = tk.Label(self.result_frame, text="Resultado de la multiplicación:", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        label_resultado.place(x=50, y=10)

        num_filas = len(resultado)
        for i, fila in enumerate(resultado):
            texto_resultado = "  ".join([f"{int(num):5}" for num in fila])
            label = tk.Label(self.result_frame, text=texto_resultado, font=("Arial", 12), bg="#f0f0f0", fg="black")
            label.place(x=50, y=40 + i * 40)
            self.result_labels.append(label)

class InversaMatrizApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Calculadora de Inversa de Matriz")
        self.root.geometry("800x600")
        self.config(bg="#3C3C3C")
        self.pack()
        self.place(x=0, y=0, width=800, height=600)
        self.widgets()

        self.filas = 0
        self.columnas = 0
        self.entradas_matriz = None
        self.result_labels = []

    def widgets(self):
        frame1 = tk.Frame(self, bg="#3C3C3C")
        frame1.place(x=0, y=0, width=800, height=600)

        titulo = tk.Label(frame1, text="Calculadora de Inversa de Matriz", font=("Arial", 18, "bold"), bg="#3C3C3C", fg="white")
        titulo.place(x=250, y=20)

        self.btn_crear_matriz = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Crear Matriz", command=self.crear_matriz)
        self.btn_crear_matriz.place(x=500, y=100, width=240, height=60)

        self.btn_inversa = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Calcular Inversa", state=tk.DISABLED, command=self.calcular_inversa)
        self.btn_inversa.place(x=500, y=200, width=240, height=60)

        self.result_frame = tk.Frame(frame1, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.result_frame.place(x=100, y=420, width=600, height=150)

        copyright_label = tk.Label(frame1, text="© 2024 PROYECTO X Code. Todos los derechos reservados", font=("Arial", 10), bg="#3C3C3C", fg="white")
        copyright_label.place(x=250, y=570)

        self.matrix_frame = tk.Frame(frame1, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.matrix_frame.place(x=30, y=90, width=450, height=320)

    def crear_matriz(self):
        try:
            self.filas = int(simpledialog.askstring("Entrada", "Número de filas para la matriz:"))
            self.columnas = int(simpledialog.askstring("Entrada", "Número de columnas para la matriz:"))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        if self.filas <= 0 or self.columnas <= 0:
            messagebox.showerror("Error", "Las filas y columnas deben ser números positivos.")
            return

        self.limpiar_entradas_matriz()

        self.entradas_matriz = [[tk.Entry(self.matrix_frame, width=5, font=("Arial", 12)) for _ in range(self.columnas)] for _ in range(self.filas)]
        for i in range(self.filas):
            for j in range(self.columnas):
                self.entradas_matriz[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.btn_inversa.config(state=tk.NORMAL)

    def limpiar_entradas_matriz(self):
        if self.entradas_matriz:
            for row in self.entradas_matriz:
                for entry in row:
                    entry.destroy()

        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

    def obtener_matriz(self, entradas, filas, columnas):
        matriz = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                try:
                    valor_entrada = float(entradas[i][j].get())
                    fila.append(valor_entrada)
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingresa valores válidos en la matriz.")
                    return None
            matriz.append(fila)
        return np.array(matriz)

    def calcular_inversa(self):
        self.matrix = self.obtener_matriz(self.entradas_matriz, self.filas, self.columnas)

        if self.matrix is None:
            return

        if self.matrix.shape[0] != self.matrix.shape[1]:
            messagebox.showerror("Error", "La matriz debe ser cuadrada para calcular su inversa.")
            return

        det = np.linalg.det(self.matrix)
        if det == 0:
            messagebox.showerror("Error", "La matriz no tiene inversa (determinante es cero).")
            return

        try:
            inversa = np.linalg.inv(self.matrix)
            self.mostrar_resultado_fracciones(inversa)
        except Exception as e:
            messagebox.showerror("Error", "No se pudo calcular la inversa. " + str(e))

    def mostrar_resultado_fracciones(self, resultado):
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

        label_resultado = tk.Label(self.result_frame, text="Resultado de la inversa:", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        label_resultado.place(x=50, y=10)

        num_filas = len(resultado)
        for i, fila in enumerate(resultado):
            texto_resultado = "  ".join([f"{Fraction(num).limit_denominator()}" for num in fila])
            label = tk.Label(self.result_frame, text=texto_resultado, font=("Arial", 12), bg="#f0f0f0", fg="black")
            label.place(x=50, y=40 + i * 40)
            self.result_labels.append(label)

class SistemaEcuacionesApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Solución de Sistema de Ecuaciones")
        self.root.geometry("800x600")
        self.config(bg="#3C3C3C")
        self.pack()
        self.place(x=0, y=0, width=800, height=600)
        self.widgets()

        self.num_ecuaciones = 0
        self.entradas_ecuaciones = None
        self.result_labels = []

    def widgets(self):
        frame1 = tk.Frame(self, bg="#3C3C3C")
        frame1.place(x=0, y=0, width=800, height=600)

        titulo = tk.Label(frame1, text="Solución de Sistema de Ecuaciones", font=("Arial", 18, "bold"), bg="#3C3C3C", fg="white")
        titulo.place(x=250, y=20)

        self.btn_crear_ecuaciones = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Crear Sistema de Ecuaciones", command=self.crear_ecuaciones)
        self.btn_crear_ecuaciones.place(x=500, y=100, width=240, height=60)

        self.btn_resolver_ecuaciones = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Resolver Sistema", state=tk.DISABLED, command=self.resolver_ecuaciones)
        self.btn_resolver_ecuaciones.place(x=500, y=200, width=240, height=60)

        self.result_frame = tk.Frame(frame1, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.result_frame.place(x=100, y=420, width=600, height=150)

        copyright_label = tk.Label(frame1, text="© 2024 PROYECTO X Code. Todos los derechos reservados", font=("Arial", 10), bg="#3C3C3C", fg="white")
        copyright_label.place(x=250, y=570)

        self.ecuaciones_frame = tk.Frame(frame1, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.ecuaciones_frame.place(x=30, y=90, width=450, height=320)

    def crear_ecuaciones(self):
        try:
            self.num_ecuaciones = int(simpledialog.askstring("Entrada", "Número de ecuaciones (y variables):"))
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")
            return

        if self.num_ecuaciones <= 0:
            messagebox.showerror("Error", "El número de ecuaciones debe ser positivo.")
            return

        self.limpiar_entradas_ecuaciones()

        self.entradas_ecuaciones = [[tk.Entry(self.ecuaciones_frame, width=5, font=("Arial", 12)) for _ in range(self.num_ecuaciones + 1)] for _ in range(self.num_ecuaciones)]
        for i in range(self.num_ecuaciones):
            for j in range(self.num_ecuaciones + 1):
                self.entradas_ecuaciones[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.btn_resolver_ecuaciones.config(state=tk.NORMAL)

    def limpiar_entradas_ecuaciones(self):
        if self.entradas_ecuaciones:
            for row in self.entradas_ecuaciones:
                for entry in row:
                    entry.destroy()

        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

    def obtener_ecuaciones(self):
        ecuaciones = []
        for i in range(self.num_ecuaciones):
            fila = []
            for j in range(self.num_ecuaciones + 1):
                try:
                    valor_entrada = float(self.entradas_ecuaciones[i][j].get())
                    fila.append(valor_entrada)
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingresa valores válidos en las ecuaciones.")
                    return None
            ecuaciones.append(fila)
        return np.array(ecuaciones)

    def resolver_ecuaciones(self):
        sistema_ecuaciones = self.obtener_ecuaciones()

        if sistema_ecuaciones is None:
            return

        A = sistema_ecuaciones[:, :-1]
        b = sistema_ecuaciones[:, -1]

        try:
            soluciones = np.linalg.solve(A, b)
            self.mostrar_resultado_ecuaciones(soluciones)
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "El sistema no tiene solución única.")
            return

    def mostrar_resultado_ecuaciones(self, soluciones):
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

        label_resultado = tk.Label(self.result_frame, text="Soluciones del sistema:", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        label_resultado.place(x=50, y=10)

        for i, solucion in enumerate(soluciones):
            label = tk.Label(self.result_frame, text=f"x{i+1} = {solucion:.2f}", font=("Arial", 12), bg="#f0f0f0", fg="black")
            label.place(x=50, y=40 + i * 30)
            self.result_labels.append(label)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("600x400+120+20")
    root.resizable(False, False)
    app = MenuPrincipal(root)
    root.mainloop()




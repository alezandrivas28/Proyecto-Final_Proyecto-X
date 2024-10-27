import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np

class MatrixCalculatorApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Calculadora de Sistemas de Ecuaciones")
        self.root.geometry("800x600")
        self.config(bg="#000000")
        self.pack()
        self.place(x=0, y=0, width=800, height=600)
        self.widgets()

        self.matrix = None
        self.vector_b = None
        self.filas = 0
        self.columnas = 0
        self.entradas_matriz = None
        self.entradas_vector = None
        self.result_labels = []  

    def widgets(self):
        frame1 = tk.Frame(self, bg="#000000")
        frame1.place(x=0, y=0, width=800, height=600)

        titulo = tk.Label(frame1, text="Calculadora de Sistemas de Ecuaciones", font=("Arial", 18, "bold"), bg="#000000", fg="white")
        titulo.place(x=250, y=20)

        self.btn_crear_matriz = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Crear Matriz y Vector", command=self.crear_matriz)
        self.btn_crear_matriz.place(x=500, y=100, width=240, height=60)

        self.btn_gauss_jordan = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Resolver por Gauss-Jordan", state=tk.DISABLED, command=self.resolver_gauss_jordan)
        self.btn_gauss_jordan.place(x=500, y=200, width=240, height=60)

        self.btn_cramer = tk.Button(frame1, bg="#8c8c8c", fg="black", font=("Arial", 12, "bold"), text="Resolver por Regla de Cramer", state=tk.DISABLED, command=self.resolver_cramer)
        self.btn_cramer.place(x=500, y=300, width=240, height=60)

        self.result_frame = tk.Frame(frame1, bg="#f0f0f0", bd=2, relief=tk.SOLID)
        self.result_frame.place(x=100, y=420, width=600, height=150)

        copyright_label = tk.Label(frame1, text="© 2024 PaluZero Code. Todos los derechos reservados", font=("Arial", 10), bg="#000000", fg="white")
        copyright_label.place(x=250, y=570)

        self.matrix_frame = tk.Frame(frame1, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.matrix_frame.place(x=30, y=90, width=450, height=320)

    def crear_matriz(self):
        try:
            self.filas = int(simpledialog.askstring("Entrada", "Número de filas para la Matriz:"))
            self.columnas = int(simpledialog.askstring("Entrada", "Número de columnas para la Matriz (debe ser igual al número de filas en el vector):"))
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

        self.entradas_vector = [tk.Entry(self.matrix_frame, width=5, font=("Arial", 12)) for _ in range(self.filas)]
        for i in range(self.filas):
            self.entradas_vector[i].grid(row=i, column=self.columnas + 1, padx=5, pady=5)

        self.btn_gauss_jordan.config(state=tk.NORMAL)
        self.btn_cramer.config(state=tk.NORMAL)

    def limpiar_entradas_matriz(self):
        if self.entradas_matriz:
            for row in self.entradas_matriz:
                for entry in row:
                    entry.destroy()
        if self.entradas_vector:
            for entry in self.entradas_vector:
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
                    messagebox.showerror("Error", "Por favor ingresa valores válidos en las matrices.")
                    return None
            matriz.append(fila)
        return np.array(matriz)

    def obtener_vector(self, entradas, filas):
        vector = []
        for i in range(filas):
            try:
                valor_entrada = float(entradas[i].get())
                vector.append(valor_entrada)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa valores válidos en el vector.")
                return None
        return np.array(vector)

    def Determinante2x2(self, A):
        """ Calcula el determinante de una matriz 2x2. """
        return A[0,0]*A[1,1] - A[0,1]*A[1,0]

    def Determinante3x3(self, A):
        """ Calcula el determinante de una matriz 3x3. """
        a = A[0,0]*A[1,1]*A[2,2]
        b = A[1,0]*A[2,1]*A[0,2]
        c = A[0,1]*A[1,2]*A[2,0]
        p = a + b + c

        a = A[2,0]*A[1,1]*A[0,2]
        b = A[1,0]*A[0,1]*A[2,2]
        c = A[2,1]*A[1,2]*A[0,0]
        n = a + b + c

        return p - n

    def resolver_gauss_jordan(self):
        try:
            self.matrix = self.obtener_matriz(self.entradas_matriz, self.filas, self.columnas)
            self.vector_b = self.obtener_vector(self.entradas_vector, self.filas)

            if self.matrix is None or self.vector_b is None:
                messagebox.showerror("Error", "Por favor ingrese todos los valores en la matriz y el vector.")
                return

            if self.matrix.shape[0] != self.matrix.shape[1]:
                messagebox.showerror("Error", "La matriz debe ser cuadrada (nxn).")
                return

            sistema = np.hstack((self.matrix, self.vector_b.reshape(-1, 1)))
            n = len(self.matrix)

            for i in range(n):
                max_row = np.argmax(abs(sistema[i:n, i])) + i
                if i != max_row:
                    sistema[[i, max_row]] = sistema[[max_row, i]]

                sistema[i] = sistema[i] / sistema[i, i]

                for j in range(i + 1, n):
                    factor = sistema[j, i]
                    sistema[j] = sistema[j] - factor * sistema[i]

            for i in range(n - 1, 0, -1):
                for j in range(i):
                    factor = sistema[j, i]
                    sistema[j] = sistema[j] - factor * sistema[i]

            solution = sistema[:, -1]
            self.mostrar_resultado(f"Solución por Gauss-Jordan:\n{self.formatear_resultados(solution)}")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al resolver el sistema: {str(e)}")

    def resolver_cramer(self):
        try:
            self.matrix = self.obtener_matriz(self.entradas_matriz, self.filas, self.columnas)
            self.vector_b = self.obtener_vector(self.entradas_vector, self.filas)

            if self.matrix is None or self.vector_b is None:
                messagebox.showerror("Error", "Por favor ingrese todos los valores en la matriz y el vector.")
                return

            if self.matrix.shape[0] == 2:
                D = self.Determinante2x2(self.matrix)
            else:
                D = self.Determinante3x3(self.matrix)

            if D == 0:
                messagebox.showerror("Error", "El determinante es cero, el sistema no tiene solución única.")
                return

            D1 = np.copy(self.matrix)
            D2 = np.copy(self.matrix)
            D3 = np.copy(self.matrix)

            D1[:, 0] = self.vector_b
            D2[:, 1] = self.vector_b

            if self.matrix.shape[0] == 2:
                d1 = self.Determinante2x2(D1)
                d2 = self.Determinante2x2(D2)
                x1 = d1 / D
                x2 = d2 / D
                self.mostrar_resultado(f"Solución por Cramer:\nx1 = {self.formatear_resultados([x1])}\nx2 = {self.formatear_resultados([x2])}")
            else:
                D3[:, 2] = self.vector_b
                d1 = self.Determinante3x3(D1)
                d2 = self.Determinante3x3(D2)
                d3 = self.Determinante3x3(D3)
                x1 = d1 / D
                x2 = d2 / D
                x3 = d3 / D
                self.mostrar_resultado(f"Solución por Cramer:\nx1 = {self.formatear_resultados([x1])}\nx2 = {self.formatear_resultados([x2])}\nx3 = {self.formatear_resultados([x3])}")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al resolver el sistema: {str(e)}")

    def formatear_resultados(self, resultados):
        """ Formatea los resultados eliminando decimales innecesarios """
        return "\n".join([str(int(r)) if r.is_integer() else f"{r:.2f}" for r in resultados])

    def mostrar_resultado(self, resultado):
        """ Mostrar el resultado en la interfaz gráfica """
        result_label = tk.Label(self.result_frame, text=resultado, font=("Arial", 14), bg="#f0f0f0")
        result_label.pack(pady=10)
        self.result_labels.append(result_label)

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()
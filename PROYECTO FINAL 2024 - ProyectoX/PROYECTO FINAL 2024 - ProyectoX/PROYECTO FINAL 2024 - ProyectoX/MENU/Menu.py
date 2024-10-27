import tkinter as tk
from tkinter import PhotoImage
import subprocess
import os

def abrir_algoritmos():
    try:
        subprocess.Popen(['python', os.path.join('index.py')])  
    except FileNotFoundError:
        print("El archivo 'index.py' no se encontró.")

def abrir_matematica_discreta():
    try:
        ruta_archivo = os.path.join(os.getcwd(), 'matediscreta1', 'matematica_discreta.py')
        subprocess.Popen(['python', ruta_archivo])  
    except FileNotFoundError:
        print("El archivo matematica_discreta.py no se encontró.")
    except Exception as e:
        print(f"Error al intentar abrir el archivo: {e}")

def abrir_algebra_lineal():
    try:
        subprocess.Popen(['python', 'algebra_lineal/menu.py'])  
    except FileNotFoundError:
        print("El archivo 'algebra_lineal/algebra_lineal.py' no se encontró.")

ventana = tk.Tk()
ventana.title("Menú de Proyectos")
ventana.geometry("600x500")  
ventana.config(bg="#000000")  

ruta_imagen_fondo = os.path.join(os.getcwd(), 'imagenes', 'fondo.jpg')

try:
    fondo_imagen = PhotoImage(file=ruta_imagen_fondo)  
    label_fondo = tk.Label(ventana, image=fondo_imagen)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
except tk.TclError:
    print("No se pudo cargar la imagen. Asegúrate de que la ruta y el archivo sean correctos.")

label_bienvenida = tk.Label(ventana, text="Selecciona un proyecto", font=("Arial", 16, "bold"), bg="#000000", fg="white")
label_bienvenida.pack(pady=20)

frame_boton = tk.Frame(ventana, bg="#000000")
frame_boton.pack(pady=20)

boton_algoritmos = tk.Button(frame_boton, text="Algoritmos", width=30, height=2, bg="#8c8c8c", font=("Arial", 12, "bold"), command=abrir_algoritmos)
boton_algoritmos.pack(pady=5)

boton_matematica_discreta = tk.Button(frame_boton, text="Matemática Discreta", width=30, height=2, bg="#8c8c8c", font=("Arial", 12, "bold"), command=abrir_matematica_discreta)
boton_matematica_discreta.pack(pady=5)

boton_algebra_lineal = tk.Button(frame_boton, text="Álgebra Lineal", width=30, height=2, bg="#8c8c8c", font=("Arial", 12, "bold"), command=abrir_algebra_lineal)
boton_algebra_lineal.pack(pady=5)

copyright_label = tk.Label(ventana, text="© 2024 PROYECTO X Code. Todos los derechos reservados", font=("Arial", 10), bg="#000000", fg="white")
copyright_label.pack(side="bottom", pady=10)

ventana.mainloop()

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class ControlClientes(tk.Frame):
    db_name = "database.db"  

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        self.configure(bg="#e3f2fd") 
        self.widgets()
        self.mostrar_clientes()

    def widgets(self):
        frame = tk.Frame(self, bg="#ffffff")  
        frame.pack(fill=tk.X, pady=20)

        tk.Label(frame, text="Código Cliente:", font="Arial 10 bold", bg="#ffffff", fg="#333").grid(row=0, column=0, padx=10, sticky="e")
        self.codigo_cliente = tk.Entry(frame, font="Arial 10", bd=2, relief="solid", fg="#333")
        self.codigo_cliente.grid(row=0, column=1, padx=10, pady=5, ipady=5)

        tk.Label(frame, text="Nombre:", font="Arial 10 bold", bg="#ffffff", fg="#333").grid(row=0, column=2, padx=10, sticky="e")
        self.nombre_cliente = tk.Entry(frame, font="Arial 10", bd=2, relief="solid", fg="#333")
        self.nombre_cliente.grid(row=0, column=3, padx=10, pady=5, ipady=5)

        tk.Label(frame, text="Dirección:", font="Arial 10 bold", bg="#ffffff", fg="#333").grid(row=0, column=4, padx=10, sticky="e")
        self.direccion_cliente = tk.Entry(frame, font="Arial 10", bd=2, relief="solid", fg="#333")
        self.direccion_cliente.grid(row=0, column=5, padx=10, pady=5, ipady=5)

        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Crear Cliente", command=self.crear_cliente, bg="#66bb6a", fg="white", font="Arial 10 bold", relief="flat", bd=0, padx=15, pady=5).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Editar Cliente", command=self.editar_cliente, bg="#ffa726", fg="white", font="Arial 10 bold", relief="flat", bd=0, padx=15, pady=5).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Eliminar Cliente", command=self.eliminar_cliente, bg="#ef5350", fg="white", font="Arial 10 bold", relief="flat", bd=0, padx=15, pady=5).grid(row=0, column=2, padx=10)

        self.tree_frame = tk.Frame(self, bg="#ffffff")
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        style = ttk.Style()
        style.configure("Treeview",
                        background="#212121",  
                        foreground="#e0e0e0", 
                        fieldbackground="#212121",  
                        font=("Arial", 10))
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background="#333",  
                        foreground="#ffffff") 
        style.map("Treeview", background=[('selected', '#3faffa')])  

        self.tree = ttk.Treeview(self.tree_frame, columns=("Código", "Nombre", "Dirección"), show="headings", height=10)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("#1", text="Código")
        self.tree.heading("#2", text="Nombre")
        self.tree.heading("#3", text="Dirección")

        self.tree.column("Código", width=100, anchor="center")
        self.tree.column("Nombre", width=200, anchor="center")
        self.tree.column("Dirección", width=300, anchor="center")

        self.tree.tag_configure('evenrow', background="#424242", foreground="#e0e0e0")
        self.tree.tag_configure('oddrow', background="#616161", foreground="#e0e0e0")

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_cliente)

    def mostrar_clientes(self):
        """Función para cargar todos los clientes en el Treeview"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM clientes")
            clientes = c.fetchall()
            for i, cliente in enumerate(clientes):
                if i % 2 == 0:
                    self.tree.insert("", "end", values=cliente, tags=('evenrow',))
                else:
                    self.tree.insert("", "end", values=cliente, tags=('oddrow',))
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los clientes: {e}")

    def seleccionar_cliente(self, event):
        """Función para seleccionar un cliente en la tabla"""
        item = self.tree.selection()
        if item:
            cliente = self.tree.item(item)["values"]
            self.codigo_cliente.delete(0, tk.END)
            self.codigo_cliente.insert(0, cliente[0])
            self.nombre_cliente.delete(0, tk.END)
            self.nombre_cliente.insert(0, cliente[1])
            self.direccion_cliente.delete(0, tk.END)
            self.direccion_cliente.insert(0, cliente[2])

    def crear_cliente(self):
        """Función para crear un nuevo cliente"""
        nombre = self.nombre_cliente.get().strip()
        direccion = self.direccion_cliente.get().strip()

        if not nombre or not direccion:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("INSERT INTO clientes (nombre, direccion) VALUES (?, ?)", (nombre, direccion))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente creado correctamente")
            self.mostrar_clientes() 
            self.limpiar_campos()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al crear el cliente: {e}")

    def editar_cliente(self):
        """Función para editar la información de un cliente"""
        cliente_id = self.codigo_cliente.get().strip()
        nombre = self.nombre_cliente.get().strip()
        direccion = self.direccion_cliente.get().strip()

        if not cliente_id or not nombre or not direccion:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("UPDATE clientes SET nombre = ?, direccion = ? WHERE codigo_cliente = ?",
                      (nombre, direccion, cliente_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.mostrar_clientes()  
            self.limpiar_campos()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar el cliente: {e}")

    def eliminar_cliente(self):
        """Función para eliminar un cliente"""
        cliente_id = self.codigo_cliente.get().strip()

        if not cliente_id:
            messagebox.showerror("Error", "Por favor, seleccione un cliente para eliminar")
            return

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("DELETE FROM clientes WHERE codigo_cliente = ?", (cliente_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.mostrar_clientes()
            self.limpiar_campos()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el cliente: {e}")

    def limpiar_campos(self):
        """Función para limpiar los campos de entrada"""
        self.codigo_cliente.delete(0, tk.END)
        self.nombre_cliente.delete(0, tk.END)
        self.direccion_cliente.delete(0, tk.END)




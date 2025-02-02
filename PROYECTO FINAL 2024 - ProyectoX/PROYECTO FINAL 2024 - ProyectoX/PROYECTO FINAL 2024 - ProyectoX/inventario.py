import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Inventario(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.widgets()

    def widgets(self):

        frame1 = tk.Frame(self, bg="#5A8F5D", highlightbackground="green", highlightthickness=3)
        frame1.pack()
        frame1.place(x=0 , y=0, width=1100, height=100)

        titulo = tk.Label(self, text="INVENTARIOS", bg="#5A8F5D", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#6BAF7D", highlightbackground="green", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        labelframe = LabelFrame(frame2, text="Productos", font="sans 22 bold", bg="#6BAF7D")
        labelframe.place(x=20, y=30, width=400, height=500)
        
        lblnombre = Label(labelframe, text="Nombre: ", font="sans 14 bold", bg="#6BAF7D")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblproveedor = Label(labelframe, text="Proveedor: ", font="sans 14 bold", bg="#6BAF7D")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold")
        self.proveedor.place(x=140, y=80, width=240, height=40)

        lblprecio = Label(labelframe, text="Precio: ", font="sans 14 bold", bg="#6BAF7D")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="sans 14 bold")
        self.precio.place(x=140, y=140, width=240, height=40)

        lblcosto = Label(labelframe, text="Costo: ", font="sans 14 bold", bg="#6BAF7D")
        lblcosto.place(x=10, y=200)
        self.costo = ttk.Entry(labelframe, font="sans 14 bold")
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label(labelframe, text="Stock: ", font="sans 14 bold", bg="#6BAF7D")
        lblstock.place(x=10, y=260)
        self.stock = ttk.Entry(labelframe, font="sans 14 bold")
        self.stock.place(x=140, y=260, width=240, height=40)

        boton_agregar = tk.Button(labelframe, text="Ingresar", font="sans 14 bold", bg="#dddddd", command=self.registrar)
        boton_agregar.place(x=80, y=340, width=240, height=40)

        boton_editar = tk.Button(labelframe, text="Editar", font="sans 14 bold", bg="#dddddd", command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=40)

        # ACA EMPIEZA LA TABLA
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=440, y=50, width=620, height=400)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=("ID","PRODUCTO","PROVEEDOR","PRECIO","COSTO","STOCK"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text="Id")
        self.tre.heading("PRODUCTO", text="Producto")
        self.tre.heading("PROVEEDOR", text="PROVEEDOR")
        self.tre.heading("PRECIO", text="Precio")
        self.tre.heading("COSTO", text="Costo")
        self.tre.heading("STOCK", text="Stock")

        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=100, anchor="center")
        self.tre.column("PROVEEDOR", width=100, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("STOCK", width=70, anchor="center")

        self.mostrar()

        btn_actualizar = Button(frame2, text="Actualizar Inventario", font="sans 14 bold", command=self.actualizar_inventario)
        btn_actualizar.place(x=440, y=480, width=260, height=50)

        boton_eliminar = tk.Button(frame2, text="Eliminar", font="sans 14 bold", bg="#dddddd", command=self.eliminar_producto)
        boton_eliminar.place(x=740, y=480, width=260, height=50)

    def eliminar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Eliminar producto", "Seleccione un producto para eliminar.")
            return
    
        item_id = self.tre.item(seleccion)["text"]  

        
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este producto?")
        if respuesta:
            try:
                consulta = "DELETE FROM inventario WHERE id=?"
                self.eje_consulta(consulta, (item_id,))

                self.renumerar_ids()

                self.tre.delete(seleccion)

                messagebox.showinfo("Eliminación exitosa", "Producto eliminado correctamente.")
            except Exception as e:
                messagebox.showwarning("Error", f"Error al eliminar el producto: {e}")

            self.mostrar()

    def renumerar_ids(self):
        """
        Función que renumera los IDs de los productos en la base de datos después de eliminar uno.
        """
        try:
            consulta = "SELECT id FROM inventario ORDER BY id"
            productos = self.eje_consulta(consulta)
        
            for nuevo_id, (producto_id,) in enumerate(productos, start=1):
                if nuevo_id != producto_id:
                    consulta_update = "UPDATE inventario SET id=? WHERE id=?"
                    self.eje_consulta(consulta_update, (nuevo_id, producto_id))
        
            consulta_reset = "UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='inventario'"
            self.eje_consulta(consulta_reset)
    
        except Exception as e:
            messagebox.showwarning("Error", f"Error al renumerar los productos: {e}")

    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    
    def validacion(self, nombre, prov, precio, costo, stock):
        if not (nombre and prov and precio and costo and stock):
            return False
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False
        return True
        
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            try:
                precio_q = "{:,.2f} Q".format(float(elem[3])) if elem[3] else ""
                costo_q = "{:,.2f} Q".format(float(elem[4])) if elem[4] else ""
            except Exception:
                precio_q, costo_q = "", ""
            self.tre.insert("", "end", iid=elem[0], text=elem[0], values=(elem[0], elem[1], elem[2], precio_q, costo_q, elem[5]))

    def actualizar_inventario(self):
        for item in self.tre.get_children():
            self.tre.delete(item)

        self.mostrar()

        messagebox.showinfo("Actualización", "El inventario ha sido actualizado correctamente")

    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        nombre = self.nombre.get()
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        if self.validacion(nombre, prov, precio, costo, stock):
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?)"
                parametros = (None, nombre, prov, precio, costo, stock)
                self.eje_consulta(consulta, parametros)
                self.mostrar()
                self.nombre.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
            except Exception as e:
                messagebox.showwarning(title="Error", message=f"Error al registrar el producto: {e}")
        else:
            messagebox.showwarning(title="Error", message="Rellene todos los campos correctamente")
            self.mostrar()

    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto para editar.")
            return
    
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]

        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#5A8F5D")

        lbl_nombre = Label(ventana_editar, text="Nombre:", font="sans 14 bold", bg="#5A8F5D")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font="sans 14 bold")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])

        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font="sans 14 bold", bg="#5A8F5D")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font="sans 14 bold")
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])

        lbl_precio = Label(ventana_editar, text="Precio:", font="sans 14 bold", bg="#5A8F5D")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font="sans 14 bold")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",", ""))

        lbl_costo = Label(ventana_editar, text="Costo:", font="sans 14 bold", bg="#5A8F5D")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font="sans 14 bold")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",", ""))

        lbl_stock = Label(ventana_editar, text="Stock:", font="sans 14 bold", bg="#5A8F5D")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font="sans 14 bold")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])

        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()

            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.")
                return

            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Ingrese valores numericos para precio y costo.")
                return

            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)
            self.mostrar()

            self.actualizar_inventario()

            ventana_editar.destroy()

        btn_guardar = Button(ventana_editar, text="Guardar cambios", font="sans 14 bold", command=guardar_cambios)
        btn_guardar.place(x=80, y=250, width=240, height=40)        
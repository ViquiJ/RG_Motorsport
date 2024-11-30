import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Credenciales predeterminadas
usuario_valido = "system"
clave_valida = "admin"
# Configuración de la ventana de inicio de sesión
root = tk.Tk()
root.title("Iniciar Sesión")
root.geometry("300x280")
root.resizable(False, False)

def iniciar_sesion():
    # Obtener el usuario y la contraseña ingresados
    usuario = entry_usuario.get()
    clave = entry_password.get()
    
    # Verificar las credenciales
    if usuario == usuario_valido and clave == clave_valida:
        root.withdraw() # Cierra la ventana de inicio de sesión
        menu_principal()  # Muestra el menú principal  
        
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def cambiar_clave():
    # Crear una nueva ventana para cambiar la contraseña
    ventana_cambiar_clave = tk.Toplevel(root)
    ventana_cambiar_clave.title("Cambiar clave")
    ventana_cambiar_clave.geometry("300x280")
    ventana_cambiar_clave.resizable(False, False)
    
    # Pedir la clave actual
    tk.Label(ventana_cambiar_clave, text="Clave actual:", font="Helvetica 12").pack(pady=5)
    clave_actual_entry = tk.Entry(ventana_cambiar_clave, show="*", width=30)
    clave_actual_entry.pack(pady=5)
    
    # Nueva clave
    tk.Label(ventana_cambiar_clave, text="Nueva clave:", font="Helvetica 12").pack(pady=5)
    nueva_clave_entry = tk.Entry(ventana_cambiar_clave, show="*", width=30)
    nueva_clave_entry.pack(pady=5)
    
    # Confirmar nueva clave
    tk.Label(ventana_cambiar_clave, text="Confirmar clave:", font="Helvetica 12").pack(pady=5)
    confirmar_clave_entry = tk.Entry(ventana_cambiar_clave, show="*", width=30)
    confirmar_clave_entry.pack(pady=5)
    
    def guardar_clave():
        global clave_valida
        clave_actual = clave_actual_entry.get()
        nueva_clave = nueva_clave_entry.get()
        confirmar_clave = confirmar_clave_entry.get()
        
        # Validar la clave actual, nueva clave y confirmación
        if clave_actual != clave_valida:
            messagebox.showerror("Error", "La clave actual es incorrecta.")
        elif not nueva_clave:
            messagebox.showerror("Error", "La nueva clave no puede estar vacía.")
        elif nueva_clave != confirmar_clave:
            messagebox.showerror("Error", "Las claves no coinciden.")
        else:
            clave_valida = nueva_clave  # Cambiar la clave válida
            messagebox.showinfo("Éxito", "Clave actualizada correctamente.")
            ventana_cambiar_clave.destroy()  # Cerrar la ventana de cambio de clave
    
    # Botón para guardar la nueva clave
    boton_guardar = tk.Button(ventana_cambiar_clave, text="Cambiar clave", font="Helvetica 12 bold", command=guardar_clave)
    boton_guardar.pack(pady=10)

def menu_principal():
    # Crear ventana del menú principal
    menu = tk.Toplevel(root)
    #menu.state(newstate="withdraw")  # Deja la ventana en estado 'withdrawn' al principio
    menu.title("RG MOTORSPORT - Menú Principal")
    menu.geometry("600x450")

    menuframe = tk.Frame(menu)
    menuframe.place(relx=0.5, rely=0.4, anchor="center")

    # Botones del menú
    boton_clientes = tk.Button(menuframe, text="CLIENTES", font="Helvetica 20 bold", bd=5, command=lambda: ventana_clientes(menu))
    boton_clientes.pack(pady=10)

    boton_vehiculos = tk.Button(menuframe, text="VEHÍCULOS", font="Helvetica 20 bold", bd=5)
    boton_vehiculos.pack(pady=10)

    boton_reparaciones = tk.Button(menuframe, text="REPARACIONES", font="Helvetica 20 bold", bd=5)
    boton_reparaciones.pack(pady=10)

    boton_proveedores = tk.Button(menuframe, text="PROVEEDORES", font="Helvetica 20 bold", bd=5)
    boton_proveedores.pack(pady=10)

    menu.mainloop()

def ventana_clientes(menu):
    # Crear la ventana de clientes
    cliente_ventana = tk.Toplevel(menu)
    cliente_ventana.title("RG MOTORSPORT - Gestión de Clientes")
    cliente_ventana.geometry("600x400")
    
    # Conexión a la base de datos
    conexion = sqlite3.connect("rgmotorsport.db")
    cursor = conexion.cursor()

    # Frame principal
    menuframe = tk.Frame(cliente_ventana, padx=20, pady=20)
    menuframe.pack(fill="both", expand=True)

    # Tabla para mostrar clientes
    tree = ttk.Treeview(menuframe, columns=("Nombre", "Apellido", "Teléfono", "Dirección", "Patente"), show="headings", height=10)
    tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    # Configuración de las cabeceras (sin la columna ID)
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Dirección", text="Dirección")
    tree.heading("Patente", text="Patente")
    
    # Configuración de las columnas
    tree.column("Nombre", width=120)
    tree.column("Apellido", width=120)
    tree.column("Teléfono", width=100)
    tree.column("Dirección", width=150)
    tree.column("Patente", width=120)

    # Botones
    agregar_button = tk.Button(menuframe, text="Agregar Cliente", command=lambda: abrir_formulario_agregar_cliente(cursor, tree))
    agregar_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    eliminar_button = tk.Button(menuframe, text="Eliminar Cliente", command=lambda: eliminar_cliente(tree, cursor))
    eliminar_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    modificar_button = tk.Button(menuframe, text="Modificar Cliente", command=lambda: abrir_formulario_modificar_cliente(tree,cursor))
    modificar_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
    # Cargar clientes al iniciar
    cargar_clientes(tree, cursor)

def cargar_clientes(tree, cursor):
    """Cargar todos los clientes desde la base de datos y mostrarlos en el TreeView."""
    # Limpiar la tabla actual
    for item in tree.get_children():
        tree.delete(item)

    # Cargar datos de la base de datos
    cursor.execute("SELECT Nombre, Apellido, Telefono, Direccion, Patente FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def abrir_formulario_agregar_cliente(cursor, tree):
    """Abrir ventana para agregar cliente."""
    formulario_ventana = tk.Toplevel(root)
    formulario_ventana.title("Agregar Cliente")
    formulario_ventana.geometry("400x300")

    # Etiquetas y campos de entrada
    tk.Label(formulario_ventana, text="Nombre:").grid(row=0, column=0, sticky="w")
    nombre_entry = tk.Entry(formulario_ventana)
    nombre_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Apellido:").grid(row=1, column=0, sticky="w")
    apellido_entry = tk.Entry(formulario_ventana)
    apellido_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Teléfono:").grid(row=2, column=0, sticky="w")
    telefono_entry = tk.Entry(formulario_ventana)
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Dirección:").grid(row=3, column=0, sticky="w")
    direccion_entry = tk.Entry(formulario_ventana)
    direccion_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Patente:").grid(row=4, column=0, sticky="w")
    # Crear un combobox con las patentes disponibles
    cursor.execute("SELECT Patente FROM vehiculos")
    patentes = [row[0] for row in cursor.fetchall()]
    patente_combobox = ttk.Combobox(formulario_ventana, values=patentes, state="readonly")
    patente_combobox.grid(row=4, column=1, padx=10, pady=5)

    def agregar_cliente():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        telefono = telefono_entry.get()
        direccion = direccion_entry.get()
        patente = patente_combobox.get()
        
        if nombre and apellido and telefono and direccion and patente:
            cursor.execute("INSERT INTO clientes (Nombre, Apellido, Telefono, Direccion, Patente) VALUES (?, ?, ?, ?, ?)",
                           (nombre, apellido, telefono, direccion, patente))
            cursor.connection.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            formulario_ventana.destroy()  # Cerrar la ventana
            cargar_clientes(tree, cursor)  # Actualizar la tabla de clientes
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")

    tk.Button(formulario_ventana, text="Agregar", command=agregar_cliente).grid(row=5, column=0, columnspan=2, pady=10)

def abrir_formulario_modificar_cliente(tree, cursor):
    """Abrir ventana para modificar cliente."""
    item_seleccionado = tree.selection()
    if not item_seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un cliente para modificar.")
        return
    
    cliente = tree.item(item_seleccionado)["values"]
    id_cliente = cliente[0]
    
    # Ventana para modificar cliente
    modificar_ventana = tk.Toplevel(root)
    modificar_ventana.title("Modificar Cliente")
    modificar_ventana.geometry("400x300")

    # Crear campos de entrada
    tk.Label(modificar_ventana, text="Nombre:").grid(row=0, column=0, sticky="w")
    nombre_entry = tk.Entry(modificar_ventana)
    nombre_entry.insert(0, cliente[0])  # Rellenar con el valor actual
    nombre_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Apellido:").grid(row=1, column=0, sticky="w")
    apellido_entry = tk.Entry(modificar_ventana)
    apellido_entry.insert(0, cliente[1])
    apellido_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Teléfono:").grid(row=2, column=0, sticky="w")
    telefono_entry = tk.Entry(modificar_ventana)
    telefono_entry.insert(0, cliente[2])
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Dirección:").grid(row=3, column=0, sticky="w")
    direccion_entry = tk.Entry(modificar_ventana)
    direccion_entry.insert(0, cliente[3])
    direccion_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Patente:").grid(row=4, column=0, sticky="w")
    patente_combobox = ttk.Combobox(modificar_ventana, values=["Patente1", "Patente2", "Patente3"])  # Llenar con las patentes disponibles
    patente_combobox.set(cliente[4])
    patente_combobox.grid(row=4, column=1, padx=10, pady=5)

    def modificar_cliente():
        nuevo_nombre = nombre_entry.get()
        nuevo_apellido = apellido_entry.get()
        nuevo_telefono = telefono_entry.get()
        nueva_direccion = direccion_entry.get()
        nueva_patente = patente_combobox.get()

        cursor.execute("""UPDATE clientes SET Nombre=?, Apellido=?, Telefono=?, Direccion=?, Patente=? 
                        WHERE ID_Cliente=?""", 
                       (nuevo_nombre, nuevo_apellido, nuevo_telefono, nueva_direccion, nueva_patente))
        cursor.connection.commit()
        messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
        cargar_clientes(tree, cursor)
        modificar_ventana.destroy()
    tk.Button(modificar_ventana, text="Modificar", command=modificar_cliente).grid(row=5, column=0, columnspan=2, pady=10)

def eliminar_cliente(tree, cursor):
    """Eliminar el cliente seleccionado en la tabla."""
    selected_item = tree.selection()
    if selected_item:
        cliente = tree.item(selected_item)["values"]
        nombre = cliente[0]
        apellido = cliente[1]
        confirm = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar al cliente {nombre} {apellido}?")
        
        if confirm:
            # Eliminar del registro en la base de datos
            cursor.execute("DELETE FROM clientes WHERE Nombre=? AND Apellido=?", (nombre, apellido))
            cursor.connection.commit()
            messagebox.showinfo("Éxito", f"Cliente {nombre} {apellido} eliminado.")
            cargar_clientes(tree, cursor)  # Actualizar la tabla de clientes
    else:
        messagebox.showerror("Error", "Por favor, selecciona un cliente para eliminar.")

# Crear un Frame para centrar todos los widgets
frame_central = tk.Frame(root)
frame_central.place(relx=0.5, rely=0.5, anchor="center")

# Agregar widgets dentro del Frame
usuario = tk.Label(frame_central, text="Administrador:", font="Helvetica 12")
usuario.pack(pady=1)

entry_usuario = tk.Entry(frame_central, width=20, font=12)
entry_usuario.pack(pady=5)

password_label = tk.Label(frame_central, text="Contraseña:", font="Helvetica 12")
password_label.pack(pady=1)

entry_password = tk.Entry(frame_central, width=20, font=12 ,show="*")
entry_password.pack(pady=5)

espacio = tk.Label(frame_central)
espacio.pack(pady=1)

# Botón de iniciar sesión
boton_ingresar = tk.Button(frame_central, text="Iniciar sesión", font="Helvetica 12 bold", command=iniciar_sesion)
boton_ingresar.pack(pady=5)

# Botón de cambiar clave
boton_cambioclave = tk.Button(frame_central, text="Cambiar clave", font="Helvetica 10 bold", command=cambiar_clave)
boton_cambioclave.pack(pady=5)

root.mainloop()
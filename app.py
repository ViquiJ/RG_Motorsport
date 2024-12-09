import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import sqlite3

# Configuración de la ventana de inicio de sesión
root = tk.Tk()
root.title("Iniciar Sesión")
root.geometry("300x280")
root.resizable(False, False)

def iniciar_sesion():
    # Obtener el usuario y la contraseña ingresados
    usuario = entry_usuario.get()
    clave = entry_password.get()
    
    conn = sqlite3.connect('rgmotorsport.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuario WHERE usuario = ? AND clave = ?", (usuario, clave))
    resultado = cursor.fetchone()
    
    if resultado:
        root.withdraw() # Cierra la ventana de inicio de sesión
        menu_principal()  # Muestra el menú principal 
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    conn.close()

# Ventana para cambiar la contraseña
def abrir_cambio_contrasena():
    ventana_cambio = tk.Toplevel()
    ventana_cambio.title("Cambiar Contraseña")
    ventana_cambio.geometry("300x250")
    ventana_cambio.resizable(False, False)
    
    #Campo clave actual
    tk.Label(ventana_cambio, text="Contraseña actual:", font="Helvetica 12").pack(pady=5)
    clave_actual_entry = tk.Entry(ventana_cambio, show="*", width=30)
    clave_actual_entry.pack(pady=5)
    
    #Campo Nueva clave
    tk.Label(ventana_cambio, text="Nueva contraseña:", font="Helvetica 12").pack(pady=5)
    nueva_clave_entry = tk.Entry(ventana_cambio, show="*", width=30)
    nueva_clave_entry.pack(pady=5)
    
    # Campo Confirmar nueva clave
    tk.Label(ventana_cambio, text="Confirmar nueva contraseña:", font="Helvetica 12").pack(pady=5)
    entry_nueva_contrasena = tk.Entry(ventana_cambio, show="*", width=30)
    entry_nueva_contrasena.pack(pady=5)

     # Botón cambiar contraseña
    tk.Button(ventana_cambio, text="Cambiar", font=20, command=lambda: cambiar_contrasena(ventana_cambio, clave_actual_entry, nueva_clave_entry, entry_nueva_contrasena)).pack(pady=10)
    ventana_cambio.mainloop()

# Función para cambiar la contraseña
def cambiar_contrasena(ventana_cambio, clave_actual_entry, nueva_clave_entry, entry_nueva_contrasena):
    clave_actual = clave_actual_entry.get()
    nueva_contrasena = nueva_clave_entry.get()
    confirmar_contrasena = entry_nueva_contrasena.get()
    
    # Validar que la clave actual no esté vacía
    if not clave_actual:
        messagebox.showerror("Error", "La contraseña actual no puede estar vacía.")
        return
    
    # Validar que la nueva contraseña no esté vacía
    if not nueva_contrasena:
        messagebox.showerror("Error", "La nueva contraseña no puede estar vacía.")
        return
    
    # Verificar que la nueva contraseña y la confirmación coincidan
    if nueva_contrasena != confirmar_contrasena:
        messagebox.showerror("Error", "La nueva contraseña y la confirmación no coinciden.")
        return
    
    conn = sqlite3.connect('rgmotorsport.db')
    cursor = conn.cursor()
    
    # Consultar la clave actual del usuario 'admin'
    cursor.execute("SELECT clave FROM usuario WHERE usuario = 'admin'")
    result = cursor.fetchone()

    if result is None:
        messagebox.showerror("Error", "No se encontró el usuario.")
        conn.close()
        return
    
    clave_guardada = result[0]

    # Verificar que la clave actual ingresada sea correcta
    if clave_actual != clave_guardada:
        messagebox.showerror("Error", "La contraseña actual es incorrecta.")
        conn.close()
        return

    # Verificar que la nueva contraseña sea diferente de la actual
    if nueva_contrasena == clave_guardada:
        messagebox.showerror("Error", "La nueva contraseña no puede ser igual a la actual.")
        conn.close()
        return

    # Actualizar la contraseña en la base de datos
    cursor.execute("UPDATE usuario SET clave = ? WHERE usuario = 'admin'", (nueva_contrasena,))
    conn.commit()
    
    messagebox.showinfo("Éxito", "Contraseña cambiada con éxito")
    conn.close()
    ventana_cambio.destroy()

def menu_principal():
    # Crear ventana del menú principal
    menu = tk.Toplevel(root)
    menu.title("RG MOTORSPORT - Menú Principal")
    menu.geometry("480x410")

    menuframe = tk.Frame(menu)
    menuframe.place(relx=0.5, rely=0.5, anchor="center")

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
    cliente_ventana.geometry("680x380")
    cliente_ventana.resizable(False, False)
    
    # Conexión a la base de datos
    conexion = sqlite3.connect("rgmotorsport.db")
    cursor = conexion.cursor()

    # Frame principal
    menuframe = tk.Frame(cliente_ventana, padx=20, pady=20)
    menuframe.pack(fill="both", expand=False)

    # Tabla para mostrar clientes
    tree = ttk.Treeview(menuframe, columns=("ID", "Nombre", "Apellido", "Teléfono", "Dirección", "Patente"), show="headings", height=10)
    tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    
    # Configuración de las cabeceras
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Dirección", text="Dirección")
    tree.heading("Patente", text="Patente")
    
    # Configuración de las columnas
    tree.column("ID", width=10)
    tree.column("Nombre", width=120)
    tree.column("Apellido", width=120)
    tree.column("Teléfono", width=100)
    tree.column("Dirección", width=150)
    tree.column("Patente", width=120)

    # Botones
    # Botón "Agregar Cliente"
    agregar_button = tk.Button(menuframe, text="Agregar Cliente",font="Helvetica 10 bold", width=35, command=lambda: abrir_formulario_agregar_cliente(cursor, tree))
    agregar_button.grid(row=5, column=0,padx=5, pady=10)

    # Botón "Modificar Cliente"
    modificar_button = tk.Button(menuframe, text="Modificar Cliente",font="Helvetica 10 bold", width=35, command=lambda: abrir_formulario_modificar_cliente(tree, cursor))
    modificar_button.grid(row=5, column=1, padx=5, pady=10)

    # Botón "Eliminar Cliente"
    eliminar_button = tk.Button(menuframe, text="Eliminar Cliente",font="Helvetica 10 bold",width=35, command=lambda: eliminar_cliente(tree, cursor))
    eliminar_button.grid(row=6, column=0, padx=5, pady=10)

    # Botón "Atrás"
    atras_button = tk.Button(menuframe, text="Atrás",font="Helvetica 10 bold", width=10, command=lambda: volver_atras(cliente_ventana, menu))
    atras_button.grid(row=6, column=1, padx=5, pady=10)
    # Cargar clientes al iniciar
    cargar_clientes(tree, cursor)
    
    def volver_atras(cliente_ventana, menu):
        cliente_ventana.destroy()  # Cerrar la ventana actual
        menu.deiconify()  # Mostrar la ventana anterior si estaba oculta
   
    menu.withdraw() # Cierra la ventana de inicio de sesión

def cargar_clientes(tree, cursor):
    """Cargar todos los clientes desde la base de datos y mostrarlos en el TreeView."""
    # Limpiar la tabla actual
    for item in tree.get_children():
        tree.delete(item)

    # Cargar datos de la base de datos
    cursor.execute("SELECT ID_Cliente, Nombre, Apellido, Telefono, Direccion, Patente FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def abrir_formulario_agregar_cliente(cursor, tree):
    """Abrir ventana para agregar cliente."""
    formulario_ventana = tk.Toplevel(root)
    formulario_ventana.title("Agregar Cliente")
    formulario_ventana.geometry("240x246")

    # Etiquetas y campos de entrada
    tk.Label(formulario_ventana, text="Nombre:").grid(row=0, column=0, sticky="w", padx=10)
    nombre_entry = tk.Entry(formulario_ventana)
    nombre_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Apellido:").grid(row=1, column=0, sticky="w", padx=10)
    apellido_entry = tk.Entry(formulario_ventana)
    apellido_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Teléfono:").grid(row=2, column=0, sticky="w", padx=10)
    telefono_entry = tk.Entry(formulario_ventana)
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Dirección:").grid(row=3, column=0, sticky="w", padx=10)
    direccion_entry = tk.Entry(formulario_ventana)
    direccion_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario_ventana, text="Patente:").grid(row=4, column=0, sticky="w", padx=10)
    # Crear un combobox con las patentes disponibles
    cursor.execute("SELECT Patente FROM vehiculos")
    patentes = [row[0] for row in cursor.fetchall()]
    patente_combobox = ttk.Combobox(formulario_ventana, values=patentes, state="readonly")
    patente_combobox.grid(row=4, column=1, padx=5, pady=5)

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

    tk.Button(formulario_ventana, text="Agregar", font="Helvetica 12 bold", width=20, command=agregar_cliente).grid(row=5, column=0, columnspan=2, pady=30)

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
    modificar_ventana.geometry("240x246")

    # Crear campos de entrada
    tk.Label(modificar_ventana, text="ID:").grid(row=0, column=0, sticky="w", padx=10)
    id_label = tk.Label(modificar_ventana, text=cliente[0])  # Mostrar el valor actual del ID
    id_label.grid(row=0, column=1, padx=10, pady=5)  # Usar un Label en vez de Entry
    
    tk.Label(modificar_ventana, text="Nombre:").grid(row=1, column=0, sticky="w", padx=10)
    nombre_entry = tk.Entry(modificar_ventana)
    nombre_entry.insert(0, cliente[1])  # Rellenar con el valor actual
    nombre_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Apellido:").grid(row=2, column=0, sticky="w", padx=10)
    apellido_entry = tk.Entry(modificar_ventana)
    apellido_entry.insert(0, cliente[2])
    apellido_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Teléfono:").grid(row=3, column=0, sticky="w", padx=10)
    telefono_entry = tk.Entry(modificar_ventana)
    telefono_entry.insert(0, cliente[3])
    telefono_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Dirección:").grid(row=4, column=0, sticky="w", padx=10)
    direccion_entry = tk.Entry(modificar_ventana)
    direccion_entry.insert(0, cliente[4])
    direccion_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(modificar_ventana, text="Patente:").grid(row=5, column=0, sticky="w", padx=10)
        # Crear un combobox con las patentes disponibles
    cursor.execute("SELECT Patente FROM vehiculos")
    patentes = [row[0] for row in cursor.fetchall()]
    patente_combobox = ttk.Combobox(modificar_ventana, values=patentes, state="readonly")
    patente_combobox.set(cliente[5])
    patente_combobox.grid(row=5, column=1, padx=10, pady=5)

    def modificar_cliente():
        nuevo_nombre = nombre_entry.get()
        nuevo_apellido = apellido_entry.get()
        nuevo_telefono = telefono_entry.get()
        nueva_direccion = direccion_entry.get()
        nueva_patente = patente_combobox.get()

        cursor.execute("""UPDATE clientes SET Nombre=?, Apellido=?, Telefono=?, Direccion=?, Patente=? 
                        WHERE ID_Cliente=?""",
                       (nuevo_nombre, nuevo_apellido, nuevo_telefono, nueva_direccion, nueva_patente, id_cliente))
        cursor.connection.commit()
        messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
        cargar_clientes(tree, cursor)
        modificar_ventana.destroy()
    tk.Button(modificar_ventana, text="Modificar", font="Helvetica 12 bold", width=20, command=modificar_cliente).grid(row=6, column=0, columnspan=2, pady=10)


def confirmar_eliminar():
    contraseña = simpledialog.askstring("Confirmación", "Por favor, ingresa tu contraseña para confirmar:", show="*")
    if contraseña is None:  # Si el usuario cancela el ingreso
        return None
    conn = sqlite3.connect('rgmotorsport.db')
    cursor = conn.cursor()
        # Consultar la clave actual del usuario 'admin'
    cursor.execute("SELECT clave FROM usuario WHERE usuario = 'admin'")
    result = cursor.fetchone()

    if result is None:
        messagebox.showerror("Error", "No se encontró el usuario.")
        conn.close()
        return
    
    clave_guardada = result[0]
    return contraseña == clave_guardada

def eliminar_cliente(tree, cursor):
    """Eliminar el cliente seleccionado en la tabla."""
    selected_item = tree.selection()
    if not selected_item:  # Verificar si se seleccionó un cliente
        messagebox.showerror("Error", "Por favor, selecciona un cliente para eliminar.")
        return
    
    cliente = tree.item(selected_item)["values"]
    nombre = cliente[1]
    apellido = cliente[2]

    # Solicitar la contraseña directamente
    resultado_confirmacion = confirmar_eliminar()
    if resultado_confirmacion is None:
        # El usuario canceló el ingreso de la contraseña, no hacemos nada
        return
    elif resultado_confirmacion:
        # Eliminar del registro en la base de datos
        cursor.execute("DELETE FROM clientes WHERE Nombre=? AND Apellido=?", (nombre, apellido))
        cursor.connection.commit()
        messagebox.showinfo("Éxito", f"Cliente {nombre} {apellido} eliminado.")
        cargar_clientes(tree, cursor)  # Actualizar la tabla de clientes
    else:
        # Si la contraseña es incorrecta
        messagebox.showerror("Acceso denegado", "Contraseña incorrecta. No se puede eliminar al cliente.")

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
boton_cambioclave = tk.Button(frame_central, text="Cambiar clave", font="Helvetica 10 bold", command=abrir_cambio_contrasena)
boton_cambioclave.pack(pady=5)

root.mainloop()
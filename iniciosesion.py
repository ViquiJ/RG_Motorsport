import tkinter as tk
from tkinter import messagebox
# Credenciales predeterminadas
usuario_valido = "system"
clave_valida = "admin"

def iniciar_sesion():
    # Obtener el usuario y la contraseña ingresados
    usuario = entry_usuario.get()
    clave = entry_password.get()
    
    # Verificar las credenciales
    if usuario == usuario_valido and clave == clave_valida:
        messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso.")
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

# Configuración de la ventana principal
root = tk.Tk()
root.title("RG MOTORSPORT")
root.geometry("300x280")
root.resizable(False, False)

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

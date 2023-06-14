import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .Comando import Comandos
from . import generic as utl

class Login():

    def __init__(self, users:dict):
        ventana = tk.Tk()
        ventana.title('Inicio de sesion')
        ventana.geometry('800x500')
        ventana.config(bg='#fcfcfc')
        ventana.resizable(width=0, height=0)
        utl.centrar_ventana(ventana, 800, 500)
        user = tk.StringVar()
        contra = tk.StringVar()

        def ingreso(root,usuario, password):  
            userEntry = usuario.get()
            passEntry = password.get()
            if (userEntry in users and passEntry == users[userEntry]):
                app = Comandos()
                app.run()
                
            elif(not userEntry or not passEntry):
                messagebox.showinfo("Atencion!", "Casillas Vacias, Ingrese su nombre de usuario y su contraseña") # Muestra un mensaje de casilla vacias
            
            else:
                messagebox.showinfo("Atencion!", "Usuario o contraseña erronea.")

        frame_form = tk.Frame(ventana, bd=0,
                              relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        frame_form_top = tk.Frame(
            frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_fill = tk.Frame(
            frame_form, height=50,  bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14), textvariable=user)
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=(
            'Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14),textvariable=contra)
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill, text="Iniciar sesion", font=(
            'Times', 15), bg='navy', bd=0, fg="#fff", command=lambda:[ingreso(ventana,user,contra)])
        inicio.pack(fill=tk.X, padx=20, pady=20)

        salir = tk.Button(frame_form_fill, text="Salir", font=(
            'Times', 15), bg='navy', bd=0, fg="#fff", command=lambda:[ventana.destroy()])
        salir.pack(fill=tk.X, padx=20, pady=20)
        ventana.mainloop()

if __name__ == '__main__':
  Login()
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import *
from tkinter import ttk
import generic as utl

class Comandos:

    
    def __init__(self, master=None):
        self.frame = tk.Tk()
        self.frame.geometry("1000x550")
        self.frame.title("Proyecto - MIA 2023")
        self.frame_consola = tk.Frame(master=self.frame, width=600, bg="sky blue")
        self.frame_consola.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.label_consola = tk.Label(master=self.frame_consola, text= "Consola", 
                                      font=("Times new roman", 20),
                                      bg = "sky blue")
        self.label_consola.place(x=20,y=20)

        self.consol = tk.Text(master=self.frame_consola, width=60, font=("Consolas",13), fg="white", bg="black")
        self.consol.place(x=40,y=60)


        self.frame_buttons = tk.Frame(master=self.frame,width=400,bg="steel blue")
        self.frame_buttons.pack(fill=tk.BOTH,side = tk.RIGHT, expand=True)

        def window_Configure():

            winC = tk.Toplevel()
            winC.title("Comando Configure")
            winC.config(width=450, height=250, bg="black")
            labelType = Label(master=winC,text="Type : ",bg="black", fg="White", font=("Constantia",14))
            labelType.place(x=15,y=20)
            entryType = ttk.Combobox(master=winC, width=30,
                state="readonly",
                values=["Local", "Cloud"],
                font=("Times New Roman",14),
                )
            entryType.place(x=80, y=25)
            
            labelEncriptL = Label(master=winC,text="Encript Log: ",bg="black", fg="White", font=("Constantia",14))
            labelEncriptL.place(x=15,y=65)
            encriptLog = ttk.Combobox(master=winC, width=30,
                state="readonly",
                values=["True", "False"],
                font=("Times New Roman",14),
                )
            encriptLog.place(x=130, y=70)

            labelEncriptR = Label(master=winC,text="Encript Read: ",bg="black", fg="White", font=("Constantia",14))
            labelEncriptR.place(x=15,y=110)
            encriptRead = ttk.Combobox(master=winC, width=30,
                state="readonly",
                values=["True", "False"],
                font=("Times New Roman",14),
                )
            encriptRead.place(x=135, y=115)

            labelLlave = Label(master=winC,text="LLave: ",bg="black", fg="White", font=("Constantia",14))
            labelLlave.place(x=15,y=155)
            encriptRead = Entry(master=winC,font=("Times New Roman",14), width=30)
            encriptRead.place(x=80, y=160)

            buttonEnvio = Button(master=winC, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=200, y=200)            

        self.button_configure = tk.Button(master = self.frame_buttons, text="Configure",
                                        width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Configure)
        self.button_configure.place(x=50,y=20)

        

        self.button_transfer = tk.Button(master = self.frame_buttons, text="Transfer",
                                        width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_transfer.place(x=220,y=20)
        self.button_create = tk.Button(master = self.frame_buttons, text="Create",
                                       width=15, height=3, font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_create.place(x=50,y=110)
        self.button_rename = tk.Button(master = self.frame_buttons,text="Rename",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black" )
        self.button_rename.place(x=220,y=110)
        self.button_delete = tk.Button(master = self.frame_buttons, text="Delete",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_delete.place(x=50,y=200)
        self.button_modify = tk.Button(master = self.frame_buttons, text="Modify",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_modify.place(x=220,y=200)
        self.button_copy = tk.Button(master = self.frame_buttons, text="Copy",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_copy.place(x=50,y=290)
        self.button_add = tk.Button(master = self.frame_buttons, text="Add",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_add.place(x=220,y=290)
        self.button_backup = tk.Button(master = self.frame_buttons, text="Backup",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_backup.place(x=50,y=380)
        self.button_exec = tk.Button(master = self.frame_buttons, text="Exec",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_exec.place(x=220,y=380)
        self.button_closeSesion = tk.Button(master = self.frame_buttons, text="Cerrar Sesion",
                                        width=15, height=3, font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_closeSesion.place(x=130,y=470)


    def run(self):
        self.frame.mainloop()


if __name__ == "__main__":
    app =Comandos()
    app.run()

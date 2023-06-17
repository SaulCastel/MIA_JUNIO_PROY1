import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from . import generic as utl
from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import filedialog
import time
from ..parser.parser import interpretCommand
from ..commands.cloud import cloud
from ..commands.log import updateLog
from .. import AES_ECB as AES

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
        self.cloudObj = cloud()

        self.parserState = {
          'encrypt_log':False,
          'encrypt_read':False,
          'configured':False,
          'message':None,
          'cloud': self.cloudObj,
          'exec': False
        }

        def getCommand(arg):
          lineStart = 'end-1c linestart'
          lineEnd = 'end-1c lineend'
          command = self.consol.get(lineStart, lineEnd).encode().decode('unicode-escape')
          self.parserState = interpretCommand(command,self.parserState)
          if self.parserState['exec']:
            params = self.parserState['exec_params']
            updateLog(str(params).strip('{}'),'input','exec',self.parserState['encrypt_log'])
            output = exec(params)
            updateLog(output,'output','exec',encrypt=self.parserState['encrypt_log'])
            self.parserState['message'] = output
            self.parserState['exec'] = False
          self.consol.insert('end', f'\n> {self.parserState["message"]}')
        
        def exec(params):
          try:
            file = open(params['path'], 'r')
          except KeyError:
            return 'Parametros invalidos'
          except FileNotFoundError:
            return 'Ruta desconocida'
          else:
            commands = []
            with file:
              commands = file.readlines()
            start = time.time()
            if self.parserState['encrypt_read']:
              for encrypted_command in commands:
                command = AES.decryptFromHex(self.parserState['key'], encrypted_command.strip())
                self.consol.insert('end', f'\n[exec in] {command}')
                self.parserState = interpretCommand(command, self.parserState)
                self.consol.insert('end', f'\n[exec out] {self.parserState["message"]}')
            else:
              for command in commands:
                self.consol.insert('end', f'\n[exec in] {command}')
                self.parserState = interpretCommand(command, self.parserState)
                self.consol.insert('end', f'\n[exec out] {self.parserState["message"]}')
            timeElapsed = '{:.2f}'.format(time.time() - start)
            return f'{len(commands)} comando(s) ejecutado(s), tiempo de procesamiento: {timeElapsed}'

        self.consol = tk.Text(master=self.frame_consola, width=60, font=("Consolas",13), fg="white", bg="black", insertbackground='white')
        self.consol.place(x=40,y=60)
        self.consol.bind('<Return>', getCommand)

        self.frame_buttons = tk.Frame(master=self.frame,width=400,bg="steel blue")
        self.frame_buttons.pack(fill=tk.BOTH,side = tk.RIGHT, expand=True)

        def window_Configure():
            winC = tk.Toplevel()
            winC.title("Comando Configure")
            winC.config(width=450, height=250, bg="black")
            #Variables para obtener comandos
            key = tk.StringVar()

            labelType = Label(master=winC,text="*Type: ",bg="black", fg="White", font=("Constantia",14))
            labelType.place(x=15,y=20)
            entryValues = ["Local", "Cloud"]
            entryType = ttk.Combobox(master=winC, width=30,
                state="readonly",
                font=("Times New Roman",14),
                )
            entryType['values'] = entryValues
            entryType.place(x=85, y=25)

            labelEncriptL = Label(master=winC,text="*Encript Log: ",bg="black", fg="White", font=("Constantia",14))
            labelEncriptL.place(x=15,y=65)
            encriptLog = ttk.Combobox(master=winC, width=30,
                state="readonly",
                values=["True", "False"],
                font=("Times New Roman",14),
                )
            encriptLog.place(x=135, y=70)

            labelEncriptR = Label(master=winC,text="*Encript Read: ",bg="black", fg="White", font=("Constantia",14))
            labelEncriptR.place(x=15,y=110)
            encriptRead = ttk.Combobox(master=winC, width=30,
                state="readonly",
                values=["True", "False"],
                font=("Times New Roman",14),
                )
            encriptRead.place(x=140, y=115)

            labelLlave = Label(master=winC,text="LLave: ",bg="black", fg="White", font=("Constantia",14))
            labelLlave.place(x=15,y=155)
            encriptRead = Entry(master=winC,font=("Times New Roman",14), width=30, textvariable=key)
            encriptRead.place(x=80, y=160)

            def obtenerDatos():
              print("Type: "+entryType.get())
              print("encript Log: "+encriptLog.get())
              print("encript Read: "+encriptRead.get())
              print("Llave: "+key.get())

            buttonEnvio = Button(master=winC, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"), command=obtenerDatos)
            buttonEnvio.place(x=200, y=200)            

        self.button_configure = tk.Button(master = self.frame_buttons, text="Configure",
                                        width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Configure)
        self.button_configure.place(x=50,y=20)
                        
        def window_Transfer():
            winT = tk.Toplevel()
            winT.title("Comando Transfer")
            winT.config(width=450, height=250, bg="black")
            From_ = tk.StringVar()
            To_ = tk.StringVar()
            labelFrom = Label(master=winT,text="*From: ",bg="black", fg="White", font=("Constantia",14))
            labelFrom.place(x=15,y=20)
            From = Entry(master=winT,font=("Constantia",14), width=20, textvariable=From_)
            From.place(x=80,y=20)
          
            labelTo = Label(master=winT,text="*To: ",bg="black", fg="White", font=("Constantia",14))
            labelTo.place(x=15,y=80)
            To = Entry(master=winT,font=("Constantia",14), width=20, textvariable=To_)
            To.place(x=65,y=85)

            labelMode = Label(master=winT,text="*Mode : ",bg="black", fg="White", font=("Constantia",14))
            labelMode.place(x=15,y=150)
            mode = ttk.Combobox(master=winT, width=30,
                state="readonly",
                values=["Local", "Cloud"],
                font=("Times New Roman",14),
                )
            mode.place(x=85, y=150)
            def obtenerdatos():
               print("From: "+From_.get())
               print("To: "+To_.get())
               print("Mode: "+mode.get())

            buttonEnvio = Button(master=winT, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=200, y=200)   

        self.button_transfer = tk.Button(master = self.frame_buttons, text="Transfer",
                                        width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command = window_Transfer)
        self.button_transfer.place(x=220,y=20)
        
        def window_Create():
            winCR = tk.Toplevel()
            winCR.title("Comando Create")
            winCR.config(width=520, height=250, bg="black")
            nombre = tk.StringVar()
            ruta = tk.StringVar()

            labelName = Label(master=winCR,text="*Name: ",bg="black", fg="White", font=("Constantia",14))
            labelName.place(x=15,y=20)
            name = Entry(master=winCR,font=("Constantia",14), width=40, textvariable=nombre)
            name.place(x=85,y=20)
            
            labelBody = Label(master=winCR,text="*Body: ",bg="black", fg="White", font=("Constantia",14))
            labelBody.place(x=15,y=60)
            body = ScrolledText(master=winCR,font=("Constantia",14), height=5, width=40)
            body.place(x=85,y=60)

            labelPath = Label(master=winCR,text="*Path : ",bg="black", fg="White", font=("Constantia",14))
            labelPath.place(x=15,y=200)
            path = Entry(master=winCR,font=("Constantia",14), width=30, textvariable=ruta)
            path.place(x=85, y=200)

            def obtenerdatos():
               print("name: "+nombre.get())
               print("body: "+body.get("1.0", tk.END))
               print("path: "+ruta.get())

            buttonEnvio = Button(master=winCR, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"), command=obtenerdatos)
            buttonEnvio.place(x=400, y=195)   

        self.button_create = tk.Button(master = self.frame_buttons, text="Create",
                                       width=15, height=3, font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Create)
        self.button_create.place(x=50,y=110)

        def window_Rename():
            winR = tk.Toplevel()
            winR.title("Comando Rename")
            winR.config(width=520, height=150, bg="black")
            ruta = tk.StringVar()
            nombre = tk.StringVar()
            labelPath = Label(master=winR,text="*Path: ",bg="black", fg="White", font=("Constantia",14))
            labelPath.place(x=15,y=20)
            path = Entry(master=winR,font=("Constantia",14), width=40)
            path.place(x=80,y=20)
            
            labelName = Label(master=winR,text="*Name: ",bg="black", fg="White", font=("Constantia",14))
            labelName.place(x=15,y=60)
            name = Entry(master=winR,font=("Constantia",14), width=40)
            name.place(x=85,y=60)

            def obtenerdatos():
               print("path: "+ruta.get())
               print("name: "+nombre.get())
               
            buttonEnvio = Button(master=winR, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=225, y=100)   
        
        self.button_rename = tk.Button(master = self.frame_buttons,text="Rename",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Rename)
        self.button_rename.place(x=220,y=110)
        
        def window_Delete():
            winD = tk.Toplevel()
            winD.title("Comando Delete")
            winD.config(width=520, height=150, bg="black")
            ruta = tk.StringVar()
            nombre = tk.StringVar()
            labelPath = Label(master=winD,text="*Path: ",bg="black", fg="White", font=("Constantia",14))
            labelPath.place(x=15,y=20)
            path = Entry(master=winD,font=("Constantia",14), width=40, textvariable=ruta)
            path.place(x=80,y=20)
            labelName = Label(master=winD,text="Name: ",bg="black", fg="White", font=("Constantia",14))
            labelName.place(x=15,y=60)
            name = Entry(master=winD,font=("Constantia",14), width=40, textvariable=nombre)
            name.place(x=80,y=60)
            def obtenerdatos():
               print("path: "+ruta.get())
               print("name: "+nombre.get())
            buttonEnvio = Button(master=winD, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=225, y=100)   
        
        self.button_delete = tk.Button(master = self.frame_buttons, text="Delete",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Delete)
        self.button_delete.place(x=50,y=200)

        def window_Modify():
            winM = tk.Toplevel()
            winM.title("Comando Modify")
            winM.config(width=520, height=250, bg="black")
            ruta = tk.StringVar()
            labelPath = Label(master=winM,text="*Path: ",bg="black", fg="White", font=("Constantia",14))
            labelPath.place(x=15,y=20)
            path = Entry(master=winM,font=("Constantia",14), width=42, textvariable=ruta)
            path.place(x=85,y=20)
            labelBody = Label(master=winM,text="*Body: ",bg="black", fg="White", font=("Constantia",14))
            labelBody.place(x=15,y=60)
            body = ScrolledText(master=winM,font=("Constantia",14), height=5, width=40)
            body.place(x=85,y=60)
            def obtenerdatos():
               print("path: "+ruta.get())
               print("body: "+body.get("1.0", tk.END))
               
            buttonEnvio = Button(master=winM, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=250, y=190)   

        self.button_modify = tk.Button(master = self.frame_buttons, text="Modify",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Modify)
        self.button_modify.place(x=220,y=200)

        def window_Copy():
            winC = tk.Toplevel()
            winC.title("Comando Copy")
            winC.config(width=300, height=160, bg="black")
            From_ = tk.StringVar()
            To_ = tk.StringVar()
            labelFrom = Label(master=winC,text="*From: ",bg="black", fg="White", font=("Constantia",14))
            labelFrom.place(x=15,y=20)
            From = Entry(master=winC,font=("Constantia",14), width=20, textvariable=From_)
            From.place(x=80,y=20)
            
            labelTo = Label(master=winC,text="*To: ",bg="black", fg="White", font=("Constantia",14))
            labelTo.place(x=15,y=70)
            To = Entry(master=winC,font=("Constantia",14), width=20, textvariable=To_)
            To.place(x=80,y=75)
            def obtenerdatos():
               print("From: "+From_.get())
               print("To: "+To_.get())
               
            buttonEnvio = Button(master=winC, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=100, y=110) 

        self.button_copy = tk.Button(master = self.frame_buttons, text="Copy",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Copy)
        self.button_copy.place(x=50,y=290)

        def window_Add():
            winA = tk.Toplevel()
            winA.title("Comando Add")
            winA.config(width=520, height=250, bg="black")
            ruta = tk.StringVar()
            labelPath = Label(master=winA,text="*Path: ",bg="black", fg="White", font=("Constantia",14))
            labelPath.place(x=15,y=20)
            path = Entry(master=winA,font=("Constantia",14), width=42, textvariable=ruta)
            path.place(x=85,y=20)
            
            labelBody = Label(master=winA,text="*Body: ",bg="black", fg="White", font=("Constantia",14))
            labelBody.place(x=15,y=60)
            body = ScrolledText(master=winA,font=("Constantia",14), height=5, width=40)
            body.place(x=85,y=60)
            def obtenerdatos():
               print("path: "+ruta.get())
               print("body: "+body.get("1.0", tk.END))
               
            buttonEnvio = Button(master=winA, text="Enviar", bg="Royal Blue", fg="White",font=("Constantia",14, "bold"))
            buttonEnvio.place(x=250, y=190) 

        self.button_add = tk.Button(master = self.frame_buttons, text="Add",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=window_Add)
        self.button_add.place(x=220,y=290)
        self.button_backup = tk.Button(master = self.frame_buttons, text="Backup",
                                       width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black")
        self.button_backup.place(x=50,y=380)

        def exec_funtionality():
            path = filedialog.askdirectory()
            name = filedialog.askopenfilename()
            print("Prueba Nombre Archivo:"+ name +"directorio: "+path)


        self.button_exec = tk.Button(master = self.frame_buttons, text="Exec",
                                    width=15, height=3,font=("Constantia",12,"bold"), fg="white", bg="black", command=exec_funtionality)
        self.button_exec.place(x=220,y=380)
        def close(self):
            self.frame.destroy()
        self.button_closeSesion = tk.Button(master = self.frame_buttons, text="Cerrar Sesion",
                                        width=15, height=3, font=("Constantia",12,"bold"), fg="white", bg="black", command=lambda:[close(self)])
        self.button_closeSesion.place(x=130,y=470)


    def run(self):
        self.frame.mainloop()

if __name__ == "__main__":
  app = Comandos()
  app.run()
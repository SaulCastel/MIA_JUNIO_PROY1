from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class cloud:
    def __init__(self):
      self.conexion()
      self.instancia()

    #Autenticar Cuenta
    def conexion(self):
        self.autenticar = GoogleAuth()
        self.autenticar.LocalWebserverAuth()
    #Creando una instancia para el manejo de los archivos y carpetas
    def instancia(self):
        self.drive = GoogleDrive(self.autenticar)
    
    def crear_subFolder(self, nombre, id_parents):    
        archivo = self.drive.CreateFile({'title':''+nombre+'', 'parents':[{'id': id_parents}],"mimeType":"application/vnd.google-apps.folder" })
        archivo.Upload()

    def crear_folder(self,nombre):
        folder = self.drive.CreateFile({'title':''+nombre+'', "mimeType":"application/vnd.google-apps.folder"})  
        folder.Upload() 

    def buscar(self,carpeta):
        listaCArchivos = self.drive.ListFile({'q': "title: '"+ carpeta +"' and trashed=false"}).GetList()
        if listaCArchivos:
            id_carpeta= listaCArchivos[0]['id'] 
            return id_carpeta

   
    def crear_Archivo(self,nombre, body, id_parents):
        archivo = self.drive.CreateFile({'title':''+ nombre +'', 'parents':[{'id': id_parents}]})
        archivo.SetContentString(body)
        archivo.Upload()

    def create(self, path, name, body) -> str:
        path = path[1:].strip()
        split = path.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass
 
        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()        
        if listaArchivos:
            print("Lista llena")
            id_anterior= listaArchivos[0]['title']
            if split:

                for x in range(0, len(split)):
                    print("carpetas"+split[x])
                    if x > 0 and split[x] != "":
                        carpeta = split[x]
                        id_anterior = self.buscar(split[x-1])
                        print("nombre carpeta :"+split[x])
                        print("nombre de anterior:"+split[x-1].strip())
                        print("Id_Anterior: "+str(id_anterior))
                        print("----------")
                        if self.buscar(split[x]):
                            print("Ya existe la carpeta")
                        else:
                            self.crear_subFolder(carpeta,id_anterior)
                            print("Subfolder creado")
                tam = len(split)
                id_carpeta = self.buscar(split[tam-1])
                self.crear_Archivo(name,body,id_carpeta)
        else: 
            print("Lista vacia")
            if split:
                
                print("Folder Raiz:" + split[0])
                self.crear_folder(split[0])
                id_anterior = self.buscar(split[0])
                for x in range(1, len(split)):
                    print("carpetas: "+split[x]+"|")
                    if x > 0:
                        carpeta = split[x]
                        id_anterior = self.buscar(split[x-1])
                        print("nombre carpeta :"+split[x])
                        print("nombre de anterior:"+split[x-1].strip())
                        print("Id_Anterior: "+str(id_anterior))
                        print("----------")
                        self.crear_subFolder(carpeta,id_anterior)
                        print("Subfolder creado")

                tam = len(split)
                print(tam)
                tam = len(split)
                id_carpeta = self.buscar(split[tam-1])
                self.crear_Archivo(name,body,id_carpeta)
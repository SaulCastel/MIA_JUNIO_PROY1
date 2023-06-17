from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class cloud:
    def __init__(self):
      self.conexion()
      self.instancia()
      id_archivo = self.buscar('Archivos')
      #listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
      #existe = listaArchivos[0]['title']     
      if id_archivo:
          print("Carpeta Raiz Existente")
      else:
          self.crear_folder("Archivos")

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
        path1 = "/archivos/"+path
        path1 = path1[1:].strip()
        split = path1.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass
 
        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            id_anterior= listaArchivos[0]['title']
            if split:
                for x in range(0, len(split)):
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
                if self.buscar(name):
                    print("El archivo ya existe")
                else:
                    id_carpeta = self.buscar(split[tam-1])
                    self.crear_Archivo(name,body,id_carpeta)
                    print("Archivo Creado Exitosamente")
        else: 
            print("Lista vacia")
            if split:
                print("Folder Raiz:" + split[0])
                self.crear_folder(split[0])
                id_anterior = self.buscar(split[0])
                for x in range(1, len(split)):
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
                if self.buscar(name):
                    print("El archivo ya existe")
                else:
                    id_carpeta = self.buscar(split[tam-1])
                    self.crear_Archivo(name,body,id_carpeta)
    
    def delete(self, path, name=None) -> str:
        print("Eliminando ......")
        path1 = "/archivos/"+path
        path1 = path1[1:].strip()
        split = path1.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass

        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            if split and name == None:
                tam = len(split)
                print(self.buscar(split[tam-1]))
                eliminarFolder = self.drive.CreateFile({'id':self.buscar(split[tam-1])})
                eliminarFolder.Delete()
                print("Carpeta Eliminada Exitosamente")
            elif split:
                eliminarArchivo = self.drive.CreateFile({'id':self.buscar(name)})
                eliminarArchivo.Delete()
                print("Archivo Eliminado Exitosamente")
                
    def rename(self, path:str, name:str ) ->str:
        path1 = "/archivos/"+path
        path1 = path1[1:].strip()
        split = path1.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass

        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            if split and self.buscar(name):
                print("Error, el nombre ya existe en otro archivo y/o Carpeta")
            elif split:
                tam = len(split)
                id_Archivo = self.buscar(split[tam-1])
                file = self.drive.CreateFile({'id':id_Archivo})
                file.FetchMetadata(fields="title") #here 404 happened
                file["title"]= name
                file.Upload()
                print("Archivo Renombrado Exitosamente")
                
    def modify(self, path:str, body:str) ->str:
        path1 = "/archivos/"+path
        path1 = path1[1:].strip()
        split = path1.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass

        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            if split:
                tam = len(split)
                id_Archivo = self.buscar(split[tam-1])
                file = self.drive.CreateFile({'id':id_Archivo})
                file.SetContentString(body)
                file.Upload()
                print("Contenido del Archivo modificado exitosamente")

    def add(self, path, body) -> str:
        path1 = "/archivos/"+path
        path1 = path1[1:].strip()
        split = path1.split("/")
        try:
            while True:
                split.remove("")
        except ValueError:
            pass

        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            if split:
                tam = len(split)
                id_Archivo = self.buscar(split[tam-1])
                file = self.drive.CreateFile({'id':id_Archivo})
                contenido = file.GetContentString()
                añadiendo = contenido + "\n" + body
                file.SetContentString(añadiendo)
                file.Upload()
                print("Contenido Añadido al Archivo Exitosamente")     

    def copiarArchivo(self,id_archivo, id_folder, nombre):
        self.drive.auth.service.files().copy(fileId=id_archivo,
                           body={"parents": [{"id": id_folder}], 'title': nombre}).execute()
    
    def copy(self, source, dest):
        origen = "/archivos/"+source
        origen = origen[1:].strip()
        splitOrigen = origen.split("/")

        destino = "/archivos/"+dest
        destino = destino[1:].strip()
        splitDestino = destino.split("/")
        try:
            while True:
                splitOrigen.remove("")
                splitDestino.remove("")
        except ValueError:
            pass
        listaArchivos = self.drive.ListFile({'q': "title contains 'Archivos' and trashed=false"}).GetList()   
        existe = listaArchivos[0]['title']     
        if listaArchivos and existe == "Archivos":
            if splitOrigen and splitDestino:
                tamO = len(splitOrigen)
                tamD = len(splitDestino)
                id_Archivo = self.buscar(splitOrigen[tamO-1])
                id_folder = self.buscar(splitDestino[tamD-1])
                type = self.drive.CreateFile({'id':id_Archivo})
                typeFile = type['mimeType']
                if typeFile == "application/vnd.google-apps.folder":
                    file_list = self.drive.ListFile({'q': "'"+id_Archivo+"' in parents and trashed=false"}).GetList()
                    for x in range(0,len(file_list)):
                        print(file_list[x]['title'], file_list[x]['id'])
                        fileOriginal = self.drive.CreateFile({'id': file_list[x]['id']})
                        nameOriginal = fileOriginal['title']
                        cambio = nameOriginal.split(".")
                        name= cambio[0] + "(copy)."+cambio[1]
                        self.copiarArchivo(file_list[x]['id'],id_folder,name)
                else:
                    fileOriginal = self.drive.CreateFile({'id': id_Archivo})
                    nameOriginal = fileOriginal['title']
                    cambio = nameOriginal.split(".")
                    newName= cambio[0] + "(copy)."+cambio[1]
                    self.copiarArchivo(id_Archivo, id_folder,newName)
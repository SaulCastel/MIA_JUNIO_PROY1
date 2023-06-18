import os
from . import config
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
        path1 = "/Archivos/"+path
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
                        if self.buscar(split[x]):
                            print("Ya existe la carpeta")
                        else:
                            self.crear_subFolder(carpeta,id_anterior)
                tam = len(split)
                if self.buscar(name):
                    return "El archivo ya existe"
                else:
                    id_carpeta = self.buscar(split[tam-1])
                    self.crear_Archivo(name,body,id_carpeta)
                    return "Archivo Creado Exitosamente"
        else: 
            if split:
                self.crear_folder(split[0])
                id_anterior = self.buscar(split[0])
                for x in range(1, len(split)):
                    if x > 0:
                        carpeta = split[x]
                        id_anterior = self.buscar(split[x-1])
                        self.crear_subFolder(carpeta,id_anterior)
                tam = len(split)
                if self.buscar(name):
                    return "El archivo ya existe"
                else:
                    id_carpeta = self.buscar(split[tam-1])
                    self.crear_Archivo(name,body,id_carpeta)
                    return "Archivo Creado Exitosamente"
    
    def delete(self, path, name=None) -> str:
        path1 = "/Archivos/"+path
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
                eliminarFolder = self.drive.CreateFile({'id':self.buscar(split[tam-1])})
                eliminarFolder.Delete()
                return "Carpeta Eliminada Exitosamente"
            elif split:
                eliminarArchivo = self.drive.CreateFile({'id':self.buscar(name)})
                eliminarArchivo.Delete()
                return "Archivo Eliminado Exitosamente"
                
    def rename(self, path:str, name:str ) ->str:
        path1 = "/Archivos/"+path
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
                return "Error, el nombre ya existe en otro archivo y/o Carpeta"
            elif split:
                tam = len(split)
                id_Archivo = self.buscar(split[tam-1])
                file = self.drive.CreateFile({'id':id_Archivo})
                file.FetchMetadata(fields="title") #here 404 happened
                file["title"]= name
                file.Upload()
                return "Archivo Renombrado Exitosamente"
                
    def modify(self, path:str, body:str) ->str:
        path1 = "/Archivos/"+path
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
                return "Contenido del Archivo modificado exitosamente"

    def add(self, path, body) -> str:
        path1 = "/Archivos/"+path
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
                return "Contenido Añadido al Archivo Exitosamente"     

    def copiarArchivo(self,id_archivo, id_folder, nombre):
        self.drive.auth.service.files().copy(fileId=id_archivo,
                           body={"parents": [{"id": id_folder}], 'title': nombre}).execute()
    
    def copy(self, source, dest)-> str:
        origen = "/Archivos/"+source
        origen = origen[1:].strip()
        splitOrigen = origen.split("/")

        destino = "/Archivos/"+dest
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
                if id_Archivo and id_folder:
                    type = self.drive.CreateFile({'id':id_Archivo})
                    typeFile = type['mimeType']
                    if typeFile == "application/vnd.google-apps.folder":
                        file_list = self.drive.ListFile({'q': "'"+id_Archivo+"' in parents and trashed=false"}).GetList()
                        for x in range(0,len(file_list)):
                            print(file_list[x]['title'], file_list[x]['id'])
                            fileOriginal = self.drive.CreateFile({'id': file_list[x]['id']})
                            nameOriginal = fileOriginal['title']
                            self.copiarArchivo(file_list[x]['id'],id_folder,nameOriginal)
                    else:
                        fileOriginal = self.drive.CreateFile({'id': id_Archivo})
                        nameOriginal = fileOriginal['title']
                        self.copiarArchivo(id_Archivo, id_folder,nameOriginal)
                elif id_Archivo == "":
                    return "Error, no existe el Archivo y/o Carpeta"
                elif id_folder == "":
                    return "Error, no existe la carpeta destino"


    def transferirArchivo(self,id_archivo, id_folder):
        archivo = self.drive.CreateFile({'id': id_archivo})
        properties = archivo['parents']
        archivo['parents'] = [{'isRoot': False, 
                       'kind': 'drive#parentReference', 
                        'id': id_folder, 
                        'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                        'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
        archivo.Upload(param={'supportsTeamDrives': True})
    
    def transfer(self, source, dest)-> str:
        origen = "/Archivos/"+source
        origen = origen[1:].strip()
        splitOrigen = origen.split("/")

        destino = "/Archivos/"+dest
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
                        self.transferirArchivo(file_list[x]['id'],id_folder)
                    return "Archivos Transferido Exitosamente"
                else:
                    self.transferirArchivo(id_Archivo, id_folder)
                    return "Archivo Transferido Exitosamente"
                
    def subir_Backup(self):
        path = config.basedir
        for carpeta in os.walk(path):
            if len(carpeta[2])>0:
                for fichero in carpeta[2]:
                    carpetas = carpeta[0].replace(os.getcwd(),"")
                    ficheroFinal = carpetas.replace("\\","/")
                    print(f' - {fichero}', ficheroFinal)
            
                    archivo = open(carpeta[0]+"/"+fichero)
                    cuerpo = archivo.read()
                    print(archivo.read())
                    self.create(ficheroFinal, fichero, cuerpo)
                    archivo.close()
        return 'Archivos enviados a la nube'
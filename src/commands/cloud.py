from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class cloud:
    
    #Autenticar Cuenta
    def conexion(self):
        self.autenticar = GoogleAuth()
        self.autenticar.LocalWebserverAuth()

    #Creando una instancia para el manejo de los archivos y carpetas
    def instancia(self):
        self.drive = GoogleDrive(self.autenticar)

    def crear_Carpeta(self, nombre):
        folder = self.drive.CreateFile({'title':'Cloud', "mimeType":"application/vnd.google-apps.folder"})  
        folder.Upload()

    def delete(self):
        listaArchivos = self.drive.ListFile({'q': "title contains 'Cloud' and trashed=false"}).GetList()
        id_carpeta= listaArchivos[0]['id'] 
        print("ID de la carpeta a eliminar en drive\n "+id_carpeta)
        eliminar = self.drive.CreateFile({'id':id_carpeta})
        eliminar.Delete()

    def crear_Archivo(self, nombre, carpeta, body):
        folder = self.drive.ListFile({'q': "title = '"+ carpeta +"' and trashed=false"}).GetList()[0]
        archivo = self.drive.CreateFile({'title':nombre, 'parents':[{'id': folder['id']}]})
        archivo.SetContentString(body)
        archivo.Upload()    

    def create(self, path, name, body):
        carpet = path
        listaArchivos = self.drive.ListFile({'q': "title contains '"+ carpet +"' and trashed=false"}).GetList()
        nombreC= listaArchivos[0]['title'] 

        if listaArchivos[0]['title'] == "":
            self.crear_Carpeta(carpet)
        else:
            self.crear_Archivo(name,nombreC,body)


from os import makedirs, getcwd
import miaProyecto1.AES_ECB as AES
from .GUI import Login

users = {}
def run():
  path = getcwd()+'/archivos/'
  makedirs(path, exist_ok=True)
  try:
    usersFile = open(path+'usuarios.txt', 'r')
  except FileNotFoundError:
    print('No se encuentra un archivo con usuarios. Terminando aplicación...')
  else:
    with usersFile:
      while True:
        user = usersFile.readline().strip()
        if not user:
          break
        password = usersFile.readline().strip()
        password = AES.decryptFromHex(b'miaproyecto12345',password)
        users[user] = password
      Login.Login(users)
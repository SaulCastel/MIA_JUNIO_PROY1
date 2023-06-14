from src.GUI import Login
import src.AES_ECB as AES
from os import makedirs

users = {}
makedirs('./archivos/', exist_ok=True)
try:
  usersFile = open('archivos/usuarios.txt', 'r')
  while True:
    user = usersFile.readline().strip()
    if not user:
      break
    password = usersFile.readline().strip()
    password = AES.decryptFromHex(b'miaproyecto12345',password)
    users[user] = password
  
  Login.Login(users)
except FileNotFoundError:
  print('No se encuentra un archivo con usuarios. Terminando aplicación...')
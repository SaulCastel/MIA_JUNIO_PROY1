from src.GUI import Login
import src.AES_ECB as AES

users = {}
with open('archivos/usuarios.txt','r') as usersFile:
  while True:
    user = usersFile.readline().strip()
    if not user:
      break
    password = usersFile.readline().strip()
    password = AES.decryptFromHex(b'miaproyecto12345',password)
    users[user] = password

Login.Login(users)
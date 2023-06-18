import miaProyecto1.AES_ECB as AES

with open('/home/saulc/encriptado.mia','r') as file:
  print(file.readline())
  decryptedText = AES.decryptFromHex(b'miaproyecto12345',file.read().strip())
  print(decryptedText)
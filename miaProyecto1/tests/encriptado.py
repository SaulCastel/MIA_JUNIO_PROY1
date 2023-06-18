import miaProyecto1.AES_ECB as AES

with open('/home/saulc/encriptado.mia','r') as file:
  print(file.readline())
  decryptedText = AES.decryptFromHex(b'miaproyecto12345',file.read().strip())
  i = 0
  for command in decryptedText.split('\n'):
    print(f'{i}. ',command)
    i += 1
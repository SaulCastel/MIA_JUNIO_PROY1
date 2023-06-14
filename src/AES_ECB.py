from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from binascii import unhexlify, hexlify

def encryptToHex(key:bytes, message:str) -> str:
  cipher = AES.new(key, AES.MODE_ECB)
  ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
  return hexlify(ct_bytes).decode('utf-8')

def decryptFromHex(key:bytes, hexStr:str) -> str:
  message = unhexlify(hexStr.encode('utf-8'))
  cipher = AES.new(key, AES.MODE_ECB)
  plainText = unpad(cipher.decrypt(message), AES.block_size)
  return plainText.decode('utf-8')
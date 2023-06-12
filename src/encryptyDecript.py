
import base64
from Crypto.Cipher import AES

def encrypt(key, data):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return cipher.nonce + tag + ciphertext
    
def decrypt(key, data):
        data = base64.b64decode(data)
        nonce = data[:AES.block_size]
        tag = data[AES.block_size:AES.block_size*2]
        ciphertext = data[AES.block_size*2:]
        cipher = AES.new(key,AES.MODE_ECB, nonce)

        return cipher.decrypt_and_verify(ciphertext,tag)




key = b'usuario1'
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext)
except ValueError:
    print("Key incorrect or message corrupted")

print(decrypt("Usuario1","686BBE3F53BF138427FFC03A64340A0C"))
import os
import shutil

basedir = os.getcwd() + "/archivos"

def create(path, name, body=None):
  path = basedir + path
  os.makedirs(path, exist_ok=True)
  file = open(path + name, "w")
  if body:
    file.write(body)
  file.close()

def delete(path, name=None):
  path = basedir + path
  try:
    if name:
     os.remove(path+name)
    else:
      shutil.rmtree(path)
  except FileNotFoundError:
    print('No se encuentra la ruta especificada')
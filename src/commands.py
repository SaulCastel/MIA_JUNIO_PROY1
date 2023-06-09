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
  if name:
    try:
      os.remove(path+name)
    except FileNotFoundError:
      print("No existe el archivo")
  else:
    shutil.rmtree(path)
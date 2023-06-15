import os
import shutil
from . import config

def create(path, name, body=None) -> str:
  path = config.basedir + path
  os.makedirs(path, exist_ok=True)
  file = open(path + name, "w")
  if body:
    file.write(body)
  file.close()
  return 'Archivo creado exitosamente'

def delete(path, name=None) -> str:
  path = config.basedir + path
  try:
    if name:
      os.remove(path+name)
      return 'Archivo eliminado'
    else:
      shutil.rmtree(path)
      return 'Ruta eliminada'
  except FileNotFoundError:
    return 'Ruta especificada no encontrada'

def add(path, body) -> str:
  path = config.basedir + path
  try:
    file = open(path,'a')
    file.write(body)
    file.close()
    return 'Archivo actualizado'
  except FileNotFoundError:
    return 'Archivo especificado no encontrado'

def modify(path:str, body:str) -> str:
  path = config.basedir + path
  try:
    file = open(path,'w')
    file.write(body)
    file.close()
    return 'Archivo modificado'
  except FileNotFoundError:
    return 'Archivo especificado no encontrado'

def rename(path:str, name:str) -> str:
  path = config.basedir + path
  pathSplit = path.rsplit('/', 1)
  newPath = ''
  if pathSplit[-1] == '':
    newPath = pathSplit[0].rsplit('/',1)[0] + f'/{name.strip("/")}/'
  else:
    newPath = pathSplit[0] + f'/{name}'
  try:
    print(path)
    print(newPath)
    os.rename(path, newPath)
    return 'Ruta renombrada'
  except FileNotFoundError:
    return 'Ruta especificada no encontrada'
  except FileExistsError:
    return 'Ruta especificada ya existe'
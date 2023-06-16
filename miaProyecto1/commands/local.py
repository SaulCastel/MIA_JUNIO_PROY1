import os
import shutil
from . import config

def configure(type, encrypt_log, encrypt_read, key=None) -> dict:
  readConfig = True if encrypt_read == 'true' else False
  logConfig = True if encrypt_log == 'true' else False
  if (readConfig or logConfig) and not key:
    raise ValueError
  configuration = {
    'type': type,
    'encrypt_log': logConfig,
    'encrypt_read': readConfig,
    'key': key.encode() if readConfig else key,
    'configured': True
  }
  return configuration

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

def copy(source, dest):
  source = config.basedir + source
  dest = config.basedir + dest
  try:
    shutil.copy(source, dest)
  except NotADirectoryError:
    pass

def add(path, body) -> str:
  path = config.basedir + path
  try:
    file = open(path, 'a')
  except FileNotFoundError:
    return 'Archivo especificado no encontrado'
  except IsADirectoryError:
    return 'Ruta especificada es un directorio'
  else:
    with file:
      file.write(body)
    return 'Archivo actualizado'

def modify(path:str, body:str) -> str:
  path = config.basedir + path
  try:
    file = open(path,'w')
  except FileNotFoundError:
    return 'Archivo especificado no encontrado'
  except IsADirectoryError:
    return 'Ruta especificada es un directorio'
  else:
    with file:
      file.write(body)
    return 'Archivo modificado'

def rename(path:str, name:str) -> str:
  path = config.basedir + path
  pathSplit = path.rsplit('/', 1)
  newPath = ''
  if pathSplit[-1] == '':
    newPath = pathSplit[0].rsplit('/',1)[0] + f'/{name.strip("/")}/'
  else:
    newPath = pathSplit[0] + f'/{name}'
  try:
    os.rename(path, newPath)
    return 'Ruta renombrada'
  except FileNotFoundError:
    return 'Ruta especificada no encontrada'
  except FileExistsError:
    return 'Ruta especificada ya existe'
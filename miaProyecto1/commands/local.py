import os
import shutil
from . import config
import re

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

def copy(source, dest) -> str:
  source = config.basedir + source
  dest = config.basedir + dest
  try:
    if not re.fullmatch(config.pathRegex, source):
      shutil.copy(source, dest)
      return 'Ruta copiada exitosamente'
    else:
      shutil.copytree(source, dest, dirs_exist_ok=True)
      return 'Ruta copiada exitosamente'
  except FileNotFoundError:
    return 'Ruta desconocida'
  except shutil.SameFileError:
    return 'No se puede usar el mismo directorio como destino'

def transfer(source, dest) -> str:
  src = config.basedir + source
  dst = config.basedir + dest
  if not re.fullmatch(config.pathRegex, dest):
    return 'Ruta destino debe ser un directorio'
  os.makedirs(dst, exist_ok=True)
  try:
    shutil.move(src, dst)
    return 'Ruta transferida exitosamente'
  except FileNotFoundError:
    return 'Ruta desconocida'
  except shutil.Error:
    renamed = renamePath(source)
    dir = config.basedir + renamed[0]
    os.makedirs(dir,exist_ok=True)
    if not re.fullmatch(config.pathRegex, source):
      with open(dir+renamed[1],'w') as file:
        file.write('')
    copy(dir, dir+renamed[1])
    if re.fullmatch(config.pathRegex, source):
      shutil.rmtree(dir)
    else:
      os.remove(dir+renamed[1])
    return 'Ruta transferida y renombrada'

def add(path, body) -> str:
  path = config.basedir + path
  try:
    file = open(path, 'a')
  except FileNotFoundError:
    return 'Ruta desconocida'
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
    return 'Ruta desconocida'
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
    return 'Ruta desconocida'
  except FileExistsError:
    return 'Ruta especificada ya existe'

def renamePath(path:str) -> tuple:
  pathSplit = path.strip('/').split('/')
  if '.' in pathSplit[-1]:
    fileSplit = pathSplit[-1].split('.')
    numberSplit = fileSplit[0].rsplit('_', 1)
    digit = '1'
    if numberSplit[-1].isdigit():
      digit = int(numberSplit[-1]) + 1
    pathSplit[-1] = numberSplit[0] + f'_{digit}.{fileSplit[1]}'
    return buildPath(pathSplit)
  else:
    numberSplit = pathSplit[-1].split('_', 1)
    digit = '1'
    if numberSplit[-1].isdigit():
      digit = int(numberSplit[-1]) + 1
    pathSplit[-1] = numberSplit[0] + f'_{digit}'
    return buildPath(pathSplit)

def buildPath(tree: list) -> tuple:
  path = ''
  for i in range(len(tree)-1):
    path += f'/{tree[i]}'
  path += '/'
  return (path, tree[-1])
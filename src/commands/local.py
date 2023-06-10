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
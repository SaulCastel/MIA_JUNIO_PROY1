import os
from datetime import datetime
from . import config

def updateLog(data:str, type:str, action:str):
  '''
  Añade una cadena formateada dentro de la bitacora actual.

  :param data: str, mensaje
  :param type: str, "input"|"output"
  :param action: str, nombre del comando ejecutado
  '''
  currDay = datetime.now()
  path = config.basedir + currDay.strftime('/logs/%Y/%m/%d/')
  os.makedirs(path, exist_ok=True)
  file = open(path+'log_archivos.txt','a')
  timeStamp = currDay.isoformat(' ', 'seconds')
  formattedStr = f'[{timeStamp}] - {type} - {action} - {data}\n'
  file.write(formattedStr)
  file.close()
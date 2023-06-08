import os

def create(path, name, body=None):
  os.makedirs(path, exist_ok=True)
  file = open(path + name, "w")
  if body:
    file.write(body)
  file.close()
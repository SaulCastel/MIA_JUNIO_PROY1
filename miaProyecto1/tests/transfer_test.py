import unittest
from ..commands.local import transfer

class TransferTest(unittest.TestCase):
  def test_create_dest_dir(self):
    kwargs = {
      'source': '/pruebas/carpeta1/hola1.txt',
      'dest': '/pruebas/carpeta_nueva/',
    }
    result = transfer(**kwargs)
    return self.assertEqual(result, 'Ruta transferida exitosamente')
  
  def test_dir_moved(self):
    kwargs = {
      'source': '/pruebas/carpeta2/',
      'dest': '/pruebas/carpeta1/',
    }
    result = transfer(**kwargs)
    return self.assertEqual(result, 'Ruta transferida exitosamente')

  def test_file_moved(self):
    kwargs = {
      'source': '/pruebas/carpeta1/hola2.txt',
      'dest': '/pruebas/carpeta3/',
    }
    result = transfer(**kwargs)
    return self.assertEqual(result, 'Ruta transferida exitosamente')

  def test_path_not_found(self):
    kwargs = {
      'source': '/pruebas/carpeta_falsa/',
      'dest': '/pruebas/carpeta1/',
    }
    result = transfer(**kwargs)
    return self.assertEqual(result, 'Ruta desconocida')

  def test_file_renamed_and_moved(self):
    kwargs = {
      'source': '/pruebas/carpeta1/carpeta2/adios1.txt',
      'dest': '/pruebas/carpeta1/carpeta2/',
    }
    result = transfer(**kwargs)
    return self.assertEqual(result, 'Ruta transferida y renombrada')

if __name__ == '__main__':
  unittest.main()
import unittest
from miaProyecto1.commands import local

class TestCopy(unittest.TestCase):
  def test_destination_not_a_directory(self):
    options = {
      'source': '/prueba2/risas.txt',
      'dest': '/test/algo.txt'
    }
    self.assertEqual(local.copy(**options), 'Destino debe ser un directorio')
  
  def test_correct_path(self):
    options = {
      'source': '/prueba2/error.txt',
      'dest': '/prueba2/'
    }
    result = local.copy(**options)
    self.assertEqual(result, 'Ruta(s) desconocida(s)')

  def test_file_copied(self):
    options = {
      'source': '/prueba2/risas.txt',
      'dest': '/prueba4/'
    }
    result = local.copy(**options)
    self.assertEqual(result,'Ruta copiada exitosamente')

  def test_same_dir_copy(self):
    options = {
      'source': '/prueba2/risas.txt',
      'dest': '/prueba2/'
    }
    result = local.copy(**options)
    self.assertEqual(result,'No se puede usar el mismo directorio como destino')

  def test_dir_copied(self):
    options = {
      'source': '/prueba4/',
      'dest': '/prueba2/'
    }
    result = local.copy(**options)
    self.assertEqual(result,'Ruta copiada exitosamente')

if __name__ == '__main__':
  unittest.main()
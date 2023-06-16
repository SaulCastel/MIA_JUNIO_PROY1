import unittest
from miaProyecto1.commands import local

class TestCopy(unittest.TestCase):
  def test_destination_not_a_directory(self):
    options = {
      'source': '/prueba2/risas.txt',
      'dest': '/prueba3/algo.txt'
    }
    self.assertRaises(NotADirectoryError, local.copy, **options)
  
  def test_correct_path(self):
    options = {
      'source': '/prueba2/error.txt',
      'dest': '/prueba2/error2.txt'
    }
    self.assertRaises(FileNotFoundError, local.copy, **options)

  def test_file_copied(self):
    options = {
      'source': '/prueba2/error.txt',
      'dest': '/prueba2/error2.txt'
    }
    result = local.copy(**options)
    self.assertEqual(result,'Archivo copiado exitosamente')

if __name__ == '__main__':
  unittest.main()
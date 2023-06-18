import unittest
from ..commands.local import renamePath

class renameFileTest(unittest.TestCase):
  def test_rename_file(self):
    result = renamePath('/hola/hola.txt')
    correct = ('/hola/', 'hola_1.txt')
    return self.assertEqual(correct, result)

  def test_rename_file_twice(self):
    result = renamePath('/hola/hola_1.txt')
    correct = ('/hola/', 'hola_2.txt')
    return self.assertEqual(correct, result)

  def test_rename_dir(self):
    result = renamePath('/hola/')
    correct = ('/', 'hola_1')
    return self.assertEqual(correct, result)

  def test_rename_dir_twice(self):
    result = renamePath('/hola_1/')
    correct = ('/', 'hola_2')
    return self.assertEqual(correct, result)

if __name__ == '__main__':
  unittest.main()
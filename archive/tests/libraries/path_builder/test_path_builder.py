import unittest
from pathlib import Path
from pathbuilder import PathBuilder  # Replace with the appropriate import statement for your PathBuilder class

class TestPathBuilder(unittest.TestCase):
    def setUp(self):
        self.initial_path = 'test_dir'
        self.builder = PathBuilder(self.initial_path)

    def test_initial_path(self):
        self.assertEqual(str(self.builder), self.initial_path)

    def test_add_method(self):
        self.builder.add('subdir')
        self.assertEqual(str(self.builder), Path(self.initial_path, 'subdir'))

    def test_create_method(self):
        self.builder.add('new_subdir')
        self.builder.create()
        self.assertTrue(Path(self.initial_path, 'new_subdir').exists())

    def tearDown(self):
        # Cleanup created directories after tests
        path = Path(self.initial_path)
        if path.exists():
            for sub_path in path.iterdir():
                if sub_path.is_dir():
                    sub_path.rmdir()
            path.rmdir()

if __name__ == '__main__':
    unittest.main()

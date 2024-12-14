import os
import unittest

import thalesians.adiutor.python_utils as python_utils

class TestPythonUtils(unittest.TestCase):
    def test_get_path_to_python_executable(self):
        path_to_python_executable = python_utils.get_path_to_python_executable()
        self.assertTrue(isinstance(path_to_python_executable, str))
        self.assertTrue(path_to_python_executable.endswith('python') or path_to_python_executable.endswith('python.exe'))
        self.assertTrue(os.path.exists(path_to_python_executable))
        
    def test_get_path_to_scripts(self):
        path_to_scripts = python_utils.get_path_to_scripts()
        self.assertTrue(isinstance(path_to_scripts, str))
        self.assertTrue(path_to_scripts.endswith('Scripts'))
        self.assertTrue(os.path.exists(path_to_scripts))
        
if __name__ == '__main__':
    unittest.main()
    
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

        self.assertTrue(isinstance(path_to_scripts, str), "path_to_scripts is not a string")
        self.assertTrue(
            path_to_scripts.endswith('Scripts') or path_to_scripts.endswith('bin'),
            f"path_to_scripts does not end with 'Scripts' or 'bin': {path_to_scripts}"
    )
        self.assertTrue(
            os.path.exists(path_to_scripts),
            f"path_to_scripts does not exist: {path_to_scripts}"
    )

        
if __name__ == '__main__':
    unittest.main()
    

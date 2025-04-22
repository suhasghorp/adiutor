"""
thalesians.adiutor.python_utils
===============================

This module provides utilities for retrieving paths related to the Python environment, 
such as the path to the Python executable and the associated `Scripts` directory.

Key Features
------------
1. **Environment Information**:
   - Retrieve the path to the currently running Python executable.
   - Locate the `Scripts` directory for the current Python installation.

Functions
---------
- **get_path_to_python_executable()**:
  - Returns the absolute path to the Python executable.

- **get_path_to_scripts()**:
  - Returns the absolute path to the `Scripts` directory of the current Python installation.

Usage
-----
### Retrieve Path to Python Executable
    >>> from thalesians.adiutor.python_utils import get_path_to_python_executable
    >>> get_path_to_python_executable()
    '/usr/bin/python3'  # Example output; may vary depending on the system

### Retrieve Path to Scripts Directory
    >>> from thalesians.adiutor.python_utils import get_path_to_scripts
    >>> get_path_to_scripts()
    '/usr/bin/Scripts'  # Example output; may vary depending on the system

Dependencies
------------
- **os**: For constructing and resolving file system paths.
- **sys**: For accessing the path of the running Python executable.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The `get_path_to_scripts` function assumes a standard directory structure for Python installations.
- The returned paths are specific to the current Python environment.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import os
import sys

def get_path_to_python_executable():
    return sys.executable

def get_path_to_scripts():
    scripts_dir = 'Scripts' if os.name == 'nt' else 'bin'
    return os.path.abspath(os.path.join(sys.prefix, scripts_dir))

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()


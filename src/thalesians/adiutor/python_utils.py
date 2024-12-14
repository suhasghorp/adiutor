import os
import sys

def get_path_to_python_executable():
    return sys.executable

def get_path_to_scripts():
    return os.path.abspath(os.path.join(os.path.dirname(get_path_to_python_executable()), 'Scripts'))

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

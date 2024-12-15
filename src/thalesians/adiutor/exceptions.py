"""
thalesians.adiutor.exceptions
=============================

This module defines custom exceptions for the `thalesians.adiutor` package. 
The primary purpose of these exceptions is to provide specialized error handling 
for numeric computations or other domain-specific operations in the library.

Classes
-------
- **NumericError**:
  - A custom exception raised for errors in numeric computations.
  - Inherits from the base Python `Exception` class for extensibility and consistency.

Usage
-----
Raising a `NumericError`:
    >>> from thalesians.adiutor.exceptions import NumericError
    >>> def divide(a, b):
    ...     if b == 0:
    ...         raise NumericError("Division by zero is not allowed.")
    ...     return a / b
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    thalesians.adiutor.exceptions.NumericError: Division by zero is not allowed.

Dependencies
------------
- None

Testing
-------
The module includes a `_test()` function for `doctest` validation.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

class NumericError(Exception):
    def __init__(self, message):
        super(NumericError, self).__init__(message)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

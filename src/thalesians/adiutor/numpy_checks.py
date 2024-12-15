"""
thalesians.adiutor.numpy_checks
===============================

This module provides utility functions for validating properties of NumPy arrays, such as size, shape, and dimensionality.
It includes predicates (`is_*` functions) to check properties and corresponding `check_*` functions to enforce these 
properties with error handling. These utilities are particularly useful for ensuring consistency in numerical computations.

Key Features
------------
1. **Size and Shape Validation**:
   - Check or enforce specific sizes and shapes of NumPy arrays.
   - Ensure compatibility between arrays with the same shape or specific dimensions.

2. **Matrix Properties**:
   - Validate whether arrays are square, rows, or columns.
   - Check the number of rows or columns in a matrix.

3. **Error Handling**:
   - Provides detailed error messages with customizable levels, leveraging the `thalesians.adiutor.checks` framework.

Functions
---------
### Size and Shape Validation
- **is_size(arg, size)**:
  - Checks if the total size of `arg` matches `size`.

- **check_size(arg, size, message='Unexpected size: ...', level=1)**:
  - Ensures the size of `arg` matches `size`. Raises an error if it doesn't.

- **is_shape(arg, shape)**:
  - Checks if the shape of `arg` matches `shape`.

- **check_shape(arg, shape, message='Unexpected shape: ...', level=1)**:
  - Ensures the shape of `arg` matches `shape`. Raises an error if it doesn't.

- **is_same_shape(arg1, arg2)**:
  - Checks if `arg1` and `arg2` have the same shape.

- **check_same_shape(arg1, arg2, message='Shapes differ: ...', level=1)**:
  - Ensures `arg1` and `arg2` have the same shape. Raises an error if they don't.

### Dimensionality Validation
- **is_ndim_1(arg)**:
  - Checks if `arg` is a one-dimensional array.

- **check_ndim_1(arg, message='Not a one-dimensional array; ...', level=1)**:
  - Ensures `arg` is one-dimensional. Raises an error if it's not.

### Matrix Properties
- **is_square(arg)**:
  - Checks if `arg` is a square matrix.

- **check_square(arg, message='Matrix is not square: ...', level=1)**:
  - Ensures `arg` is a square matrix. Raises an error if it's not.

- **is_row(arg)**:
  - Checks if `arg` is a row vector.

- **check_row(arg, message='Matrix is not a row: ...', level=1)**:
  - Ensures `arg` is a row vector. Raises an error if it's not.

- **is_col(arg)**:
  - Checks if `arg` is a column vector.

- **check_col(arg, message='Matrix is not a column: ...', level=1)**:
  - Ensures `arg` is a column vector. Raises an error if it's not.

### Row and Column Validation
- **is_nrow(arg, nrow)**:
  - Checks if `arg` has `nrow` rows.

- **check_nrow(arg, nrow, message='Unexpected number of rows: ...', level=1)**:
  - Ensures `arg` has `nrow` rows. Raises an error if it doesn't.

- **is_ncol(arg, ncol)**:
  - Checks if `arg` has `ncol` columns.

- **check_ncol(arg, ncol, message='Unexpected number of columns: ...', level=1)**:
  - Ensures `arg` has `ncol` columns. Raises an error if it doesn't.

Dependencies
------------
- **NumPy**: For array manipulation and property checks.
- **thalesians.adiutor.checks**: For enforcing conditions with customizable error messages.
- **thalesians.adiutor.numpy_utils**: Provides auxiliary functions like `npu.nrow` and `npu.ncol` for row/column validation.

Usage
-----
### Checking Size
    >>> import numpy as np
    >>> from thalesians.adiutor.numpy_checks import is_size, check_size
    >>> arr = np.array([1, 2, 3, 4])
    >>> is_size(arr, 4)
    True
    >>> check_size(arr, 3)
    Traceback (most recent call last):
        ...
    AssertionError: Unexpected size: actual=4, expected=3

### Validating Shape
    >>> arr = np.array([[1, 2], [3, 4]])
    >>> is_shape(arr, (2, 2))
    True
    >>> check_shape(arr, (2, 3))
    Traceback (most recent call last):
        ...
    AssertionError: Unexpected shape: actual=(2, 2), expected=(2, 3)

### Ensuring Square Matrix
    >>> is_square(np.array([[1, 2], [3, 4]]))
    True
    >>> check_square(np.array([[1, 2, 3], [4, 5, 6]]))
    Traceback (most recent call last):
        ...
    AssertionError: Matrix is not square: (2, 3)

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The `check_*` functions are particularly useful in environments where strict validation is required.
- These utilities integrate seamlessly with the rest of the `thalesians.adiutor` package.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import numpy as np

from thalesians.adiutor.checks import check
import thalesians.adiutor.numpy_utils as npu

def is_size(arg, size):
    return np.size(arg) == size

def check_size(arg, size, message='Unexpected size: actual=%(actual)d, expected=%(expected)d', level=1):
    n = np.size(arg)
    check(n == size, message=lambda: message % {'actual': n, 'expected': size}, level=level)
    return arg

def is_shape(arg, shape):
    return np.shape(arg) == shape

def check_shape(arg, shape, message='Unexpected shape: actual=%(actual)s, expected=%(expected)s', level=1):
    s = np.shape(arg)
    check(s == shape, message=lambda: message % {'actual': s, 'expected': shape}, level=level)
    return arg

def is_same_shape(arg1, arg2):
    return np.shape(arg1) == np.shape(arg2)

def check_same_shape(arg1, arg2, message='Shapes differ: %(shape1)s vs %(shape2)s', level=1):
    s1 = np.shape(arg1); s2 = np.shape(arg2)
    check(s1 == s2, message=lambda: message % {'shape1': s1, 'shape2': s2}, level=level)
    return s1

def is_ndim_1(arg):
    return len(np.shape(arg)) == 1

def check_ndim_1(arg, message='Not a one-dimensional array; number of dimensions: %(actual)d', level=1):
    n = np.ndim(arg)
    check(n == 1, message=lambda: message % {'actual': n}, level=level)
    return arg

def is_square(arg):
    if np.size(arg) == 1: return True
    s = np.shape(arg)
    return len(s) == 2 and s[0] == s[1]

def check_square(arg, message='Matrix is not square: %(actual)s', level=1):
    if np.size(arg) > 1:
        s = np.shape(arg)
        check(len(s) == 2 and s[0] == s[1], message=lambda: message % {'actual': s}, level=level)
    return arg

def is_row(arg):
    s = np.shape(arg)
    return len(s) == 2 and s[0] == 1

def check_row(arg, message='Matrix is not a row: %(actual)s', level=1):
    s = np.shape(arg)
    check(len(s) == 2 and s[0] == 1, message=lambda: message % {'actual': s}, level=level)
    return arg

def is_col(arg):
    s = np.shape(arg)
    return len(s) == 2 and s[1] == 1
    
def check_col(arg, message='Matrix is not a column: %(actual)s', level=1):
    s = np.shape(arg)
    check(len(s) == 2 and s[1] == 1, message=lambda: message % {'actual': s}, level=level)
    return arg

def is_nrow(arg, nrow):
    return npu.nrow(arg) == nrow

def check_nrow(arg, nrow, message='Unexpected number of rows: actual=%(actual)d, expected=%(expected)d', level=1):
    n = npu.nrow(arg)
    check(n == nrow, message=lambda: message % {'actual': n, 'expected': nrow}, level=level)
    return arg

def is_ncol(arg, ncol):
    return npu.ncol(arg) == ncol

def check_ncol(arg, ncol, message='Unexpected number of columns: actual=%(actual)d, expected=%(expected)d', level=1):
    n = npu.ncol(arg)
    check(n == ncol, message=lambda: message % {'actual': n, 'expected': ncol}, level=level)
    return arg

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

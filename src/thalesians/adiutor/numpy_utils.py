"""
thalesians.adiutor.numpy_utils
==============================

This module provides an extensive set of utilities for working with NumPy arrays. 
It includes functions for array manipulation, dimensionality adjustments, symmetry enforcement, 
and vectorized operations. The utilities are designed to enhance flexibility and efficiency when 
working with numerical data.

Key Features
------------
1. **Dimensionality Utilities**:
   - Convert arrays to specific dimensions (`to_ndim_1`, `to_ndim_2`).
   - Create rows, columns, and matrices with specified values or dimensions.

2. **Symmetry Operations**:
   - Enforce lower or upper triangular symmetry in arrays.

3. **Array Properties**:
   - Check if arrays are views of each other.
   - Extract row and column counts (`nrow`, `ncol`).

4. **Vectorized Operations**:
   - Decorate functions for vectorized behavior.
   - Efficiently apply functions to arrays (`apply`).

5. **Matrix Utilities**:
   - Perform Kronecker sums.
   - Reshape arrays with vectorization (`vec`, `unvec`).

6. **Top-N Retention**:
   - Retain the largest `n` elements in an array while zeroing out the rest.

7. **Immutability**:
   - Make arrays immutable or create immutable copies.

Functions
---------
### Dimensionality Utilities
- **to_ndim_1(arg, copy=False)**:
  - Converts an array to 1D.

- **to_ndim_2(arg, ndim_1_to_col=False, copy=False)**:
  - Converts an array to 2D. Optionally reshapes 1D arrays into columns.

- **row(*args)**:
  - Creates a single-row matrix from the input.

- **col(*args)**:
  - Creates a single-column matrix from the input.

- **matrix(ncol, *args)**:
  - Creates a matrix with `ncol` columns from the input.

- **matrix_of(nrow, ncol, val)**:
  - Creates a matrix of dimensions `(nrow, ncol)` filled with `val`.

### Symmetry Operations
- **lower_to_symmetric(a, copy=False)**:
  - Enforces symmetry by copying the lower triangular part to the upper part.

- **upper_to_symmetric(a, copy=False)**:
  - Enforces symmetry by copying the upper triangular part to the lower part.

### Array Properties
- **nrow(arg)**:
  - Returns the number of rows in an array.

- **ncol(arg)**:
  - Returns the number of columns in an array.

- **is_view_of(arg1, arg2)**:
  - Checks if `arg1` is a view of `arg2`.

- **are_views_of_same(arg1, arg2)**:
  - Checks if `arg1` and `arg2` are views of the same base array.

### Vectorized Operations
- **vectorized(func)**:
  - Decorates a function to indicate it supports vectorized operations.

- **is_vectorized(func)**:
  - Checks if a function is marked as vectorized.

### Top-N Retention
- **keep_top_n(arr, top_n)**:
  - Retains the top `n` elements in a NumPy array, zeroing out the rest.

### Immutability
- **make_immutable(arg, allow_none=False)**:
  - Makes an array immutable by disabling write access.

- **immutable_copy_of(arg)**:
  - Returns an immutable copy of the input array.

### Other Utilities
- **apply(func, arg, dtype='float64')**:
  - Applies a function element-wise to an array.

- **kron_sum(arg1, arg2)**:
  - Computes the Kronecker sum of two matrices.

- **vec(arg)**:
  - Flattens an array into a column vector.

- **unvec(arg, nrow)**:
  - Reshapes a column vector back into a matrix with `nrow` rows.

Dependencies
------------
- **NumPy**: For core array manipulations.
- **thalesians.adiutor.checks**: For array validation and error handling.
- **thalesians.adiutor.utils**: For batching and auxiliary utilities.

Usage
-----
### Adjusting Dimensions
    >>> import numpy as np
    >>> from thalesians.adiutor.numpy_utils import to_ndim_1, to_ndim_2
    >>> arr = np.array([[1, 2], [3, 4]])
    >>> to_ndim_1(arr)
    array([1, 2, 3, 4])
    >>> to_ndim_2(arr)
    array([[1, 2],
           [3, 4]])

### Enforcing Symmetry
    >>> from thalesians.adiutor.numpy_utils import lower_to_symmetric
    >>> arr = np.array([[1, 0], [2, 3]])
    >>> lower_to_symmetric(arr)
    array([[1, 2],
           [2, 3]])

### Retaining Top N Elements
    >>> from thalesians.adiutor.numpy_utils import keep_top_n
    >>> arr = np.array([1, 5, 3, 7, 2])
    >>> keep_top_n(arr, 2)
    array([0, 5, 0, 7, 0])

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- Immutability functions are particularly useful for preventing unintended modifications to shared data.
- Top-N retention can be applied to both 1D and multi-dimensional arrays.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import datetime as dt
import warnings

import numpy as np

import thalesians.adiutor.checks as checks
import thalesians.adiutor.utils as utils

def init_warnings():
    np.warnings.filterwarnings('ignore', message='Mean of empty slice')
    np.warnings.filterwarnings('ignore', message='All-NaN axis encountered')
    warnings.filterwarnings('ignore', message='Warning: converting a masked element to nan.')

def apply(func, arg, dtype='float64'):
    result = np.empty(np.shape(arg), dtype=dtype)
    result.flat[:] = [func(x) for x in arg.flat[:]]
    return result

def sign(arg):
    if isinstance(arg, dt.timedelta):
        arg = arg.total_seconds()
    elif checks.is_numpy_array(arg) and arg.dtype == object and np.size(arg) > 0 and isinstance(arg.item(0), dt.timedelta):
        arg = np.vectorize(lambda x: x.total_seconds())(arg)
    return np.sign(arg)

def is_view_of(arg1, arg2):
    if not checks.is_numpy_array(arg1) or not checks.is_numpy_array(arg2):
        return False
    return arg1.base is arg2

def are_views_of_same(arg1, arg2):
    if not checks.is_numpy_array(arg1) or not checks.is_numpy_array(arg2):
        return False
    return (arg1.base is arg2) or (arg2.base is arg1) or ((arg1.base is arg2.base) and arg1.base is not None)
    
def nrow(arg):
    return np.shape(arg)[0]

def ncol(arg):
    return np.shape(arg)[1]

def to_scalar(arg, raise_value_error=True):
    try:
        if checks.is_float(arg): return arg
        elif checks.is_numpy_array(arg): return arg.item()
        else: return np.array(arg).item()
    except:
        if raise_value_error: raise
        return arg

def to_ndim_1(arg, copy=False):
    r = np.reshape(arg, (np.size(arg),))
    if r.base is arg and copy: r = np.copy(r)
    return r

def to_ndim_2(arg, ndim_1_to_col=False, copy=False):
    r = np.ndim(arg)
    if r == 0: arg = np.array(((arg,),))
    elif r == 1:
        arg = np.array((arg,))
        if ndim_1_to_col: arg = arg.T
    if copy:
        return np.array(arg, copy=copy)
    else:
        return np.asarray(arg)    

def row(*args):
    return to_ndim_2(args, ndim_1_to_col=False)

def col(*args):
    return to_ndim_2(args, ndim_1_to_col=True)

def matrix(ncol, *args):
    return np.array(utils.batch(ncol, args))

def matrix_of(nrow, ncol, val):
    r = np.empty((nrow, ncol))
    r.fill(val)
    return r

def row_of(n, val):
    return matrix_of(1, n, val)

def col_of(n, val):
    return matrix_of(n, 1, val)

def ndim_1_of(n, val):
    r = np.empty((n,))
    r.fill(val)
    return r

def make_immutable(arg, allow_none=False):
    if allow_none and arg is None: return None
    checks.check_numpy_array(arg)
    arg.flags.writeable = False
    return arg

def immutable_copy_of(arg):
    if checks.is_numpy_array(arg):
        result = np.copy(arg) if arg.flags.writeable else arg
    else:
        result = np.array(arg)
    result.flags.writeable = False
    return result
        
def lower_to_symmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[idxs] = a[(idxs[1], idxs[0])]
    return a

def upper_to_symmetric(a, copy=False):
    a = np.copy(a) if copy else a
    idxs = np.triu_indices_from(a)
    a[(idxs[1], idxs[0])] = a[idxs]
    return a

def kron_sum(arg1, arg2):
    return np.kron(arg1, np.eye(nrow(arg2))) + np.kron(np.eye(nrow(arg1)), arg2)

def vec(arg):
    return np.resize(to_ndim_2(arg, ndim_1_to_col=True, copy=False).T, (np.size(arg), 1))

def unvec(arg, nrow):
    return np.resize(to_ndim_1(arg, copy=False), (np.size(arg) // nrow, nrow)).T

def vectorized(func):
    func.__dict__['vectorized'] = True
    return func

def is_vectorized(func):
    res = False
    if hasattr(func, '__call__'):
        if hasattr(func.__call__, '__dict__'):
            res |= func.__call__.__getattribute__('__dict__').get('vectorized', False)
    if not res and hasattr(func, '__dict__'):
        res = func.__getattribute__('__dict__').get('vectorized', False)
    return res

def keep_top_n(arr, top_n):
    """
    Retain the top `n` elements in a NumPy array, zeroing out the rest.
    
    Parameters:
    - arr (numpy.ndarray): The input array.
    - top_n (int): Number of top elements to retain.
    
    Returns:
    - numpy.ndarray: Array with only the top `n` elements retained.
    """
    # Flatten the array to handle multi-dimensional arrays
    flat_arr = arr.flatten()
    
    # Get the indices of the top_n largest elements
    top_indices = np.argpartition(flat_arr, -top_n)[-top_n:]
    
    # Create a mask for the top_n elements
    mask = np.zeros_like(flat_arr, dtype=bool)
    mask[top_indices] = True
    
    # Retain the top_n elements and zero out the rest
    result = np.zeros_like(flat_arr)
    result[mask] = flat_arr[mask]
    
    # Reshape back to the original shape
    return result.reshape(arr.shape)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

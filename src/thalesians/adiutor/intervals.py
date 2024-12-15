"""
thalesians.adiutor.intervals
============================

This module provides a class for working with mathematical intervals, allowing the representation 
and manipulation of intervals with customizable boundary conditions (open or closed). The `Interval` 
class is designed to be flexible and intuitive, supporting basic operations like comparison, 
replacement of bounds, and string representation.

Classes
-------
- **Interval**:
  - Represents a mathematical interval.
  - Supports open and closed boundaries on both ends.
  - Provides methods for replacing boundaries and comparison.

Features
--------
1. **Customizable Boundaries**:
   - Left and right boundaries can be open or closed.
   - Allows precise representation of intervals.

2. **Replacement Methods**:
   - Replace the left or right boundary while retaining or modifying its closed/open status.

3. **Equality Comparison**:
   - Two intervals are considered equal if their boundaries and open/closed statuses are identical.

4. **String Representation**:
   - Provides a concise string representation of intervals, e.g., `[1, 5)` for a half-open interval.

Class: Interval
---------------
### Constructor
- **`Interval(left, right, left_closed=False, right_closed=False)`**:
  - Initializes an interval with specified boundaries and their open/closed statuses.

### Properties
- **`left`**:
  - Returns the left boundary.
- **`right`**:
  - Returns the right boundary.
- **`left_closed`**:
  - Indicates whether the left boundary is closed.
- **`right_closed`**:
  - Indicates whether the right boundary is closed.

### Methods
- **`replace_left(new_left, new_left_closed=None)`**:
  - Returns a new `Interval` with a replaced left boundary and optionally a new closed/open status.

- **`replace_right(new_right, new_right_closed=None)`**:
  - Returns a new `Interval` with a replaced right boundary and optionally a new closed/open status.

- **`__eq__(other)`**:
  - Compares two intervals for equality based on boundaries and their open/closed statuses.

- **`__str__()`**:
  - Returns a string representation of the interval (e.g., `[1, 5)`).

- **`__repr__()`**:
  - Returns the same string representation as `__str__()`.

Usage
-----
Creating and manipulating intervals:
    >>> interval = Interval(1, 5, left_closed=True, right_closed=False)
    >>> print(interval)
    [1, 5)

Replacing boundaries:
    >>> new_interval = interval.replace_left(0)
    >>> print(new_interval)
    [0, 5)

Equality comparison:
    >>> interval1 = Interval(1, 5, left_closed=True, right_closed=False)
    >>> interval2 = Interval(1, 5, left_closed=True, right_closed=False)
    >>> interval1 == interval2
    True

Dependencies
------------
- **io**: Used for efficient string concatenation during interval string representation.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import io

class Interval(object):
    def __init__(self, left, right, left_closed=False, right_closed=False):
        self._left = left
        self._right = right
        self._left_closed = left_closed
        self._right_closed = right_closed
        self._str_Interval = None
        
    @property
    def left(self):
        return self._left
        
    @property
    def right(self):
        return self._right
    
    @property
    def left_closed(self):
        return self._left_closed
    
    @property
    def right_closed(self):
        return self._right_closed
        
    def replace_left(self, new_left, new_left_closed=None):
        if new_left_closed is None: new_left_closed = self._left_closed
        return Interval(new_left, self._right, new_left_closed, self._right_closed)
    
    def replace_right(self, new_right, new_right_closed=None):
        if new_right_closed is None: new_right_closed = self._right_closed
        return Interval(self._left, new_right, self._left_closed, new_right_closed)
    
    def __eq__(self, other):
        return self._left == other.left and self._right == other.right and \
            self._left_closed == other.left_closed and self._right_closed == other.right_closed
    
    def __str__(self):
        if self._str_Interval is None:
            s = io.StringIO()
            s.write('[' if self._left_closed else '(')
            s.write(str(self._left))
            s.write(', ')
            s.write(str(self._right))
            s.write(']' if self._right_closed else ')')
            self._str_Interval = s.getvalue()
        return self._str_Interval
                
    def __repr__(self):
        return str(self)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

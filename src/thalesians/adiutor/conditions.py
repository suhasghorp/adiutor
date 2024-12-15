"""
thalesians.adiutor.conditions
=============================

This module provides decorators to enforce preconditions and postconditions on functions and methods. 
Preconditions validate the input arguments of a function before execution, while postconditions validate 
the output after execution. These decorators are particularly useful for ensuring that a function adheres 
to its contract in terms of input-output relationships, promoting reliability and robustness in the code.

Key Features
------------
1. **Preconditions**:
   - Verify that function inputs meet specific criteria before execution.
   - Automatically raise errors if inputs are invalid, with customizable messages and levels.

2. **Postconditions**:
   - Verify that function outputs meet specific criteria after execution.
   - Automatically raise errors if outputs are invalid, with customizable messages and levels.

3. **Flexible Configuration**:
   - Allows fine-grained control over which checks (preconditions, postconditions, or both) are enforced, 
     based on configurable levels (`our_config.MIN_PRECONDITION_LEVEL` and `our_config.MIN_POSTCONDITION_LEVEL`).

Functions
---------
- **conditions(pre=None, post=None, message='Condition violated', level=1)**:
   - A decorator that enforces both preconditions and postconditions on a function.
   - `pre`: A callable that evaluates a condition on input arguments.
   - `post`: A callable that evaluates a condition on the return value.
   - `message`: Customizable error message for violations.
   - `level`: The enforcement level, allowing checks to be skipped based on configuration.

- **precondition(check, message='Precondition violated', level=1)**:
   - A decorator that enforces a precondition on a function.

- **postcondition(check, message='Postcondition violated', level=1)**:
   - A decorator that enforces a postcondition on a function.

Usage
-----
### Enforcing Preconditions and Postconditions
Example usage of `conditions` to ensure function contract compliance:

    >>> from thalesians.adiutor.conditions import conditions
    >>> @conditions(pre=lambda x: x > 0, post=lambda retval: retval % 2 == 0, message="Invalid condition")
    ... def double_even(x):
    ...     return x * 2
    ...
    >>> double_even(5)
    Traceback (most recent call last):
        ...
    AssertionError: Invalid condition

### Using Precondition or Postcondition Separately
Enforcing only a precondition:
    >>> from thalesians.adiutor.conditions import precondition
    >>> @precondition(lambda x: x > 0, message="Input must be positive")
    ... def square(x):
    ...     return x ** 2
    ...
    >>> square(-2)
    Traceback (most recent call last):
        ...
    AssertionError: Input must be positive

Enforcing only a postcondition:
    >>> from thalesians.adiutor.conditions import postcondition
    >>> @postcondition(lambda retval: retval > 0, message="Result must be positive")
    ... def decrement(x):
    ...     return x - 1
    ...
    >>> decrement(0)
    Traceback (most recent call last):
        ...
    AssertionError: Result must be positive

Dependencies
------------
- **thalesians.adiutor.checks**: Provides the `check` function for evaluating conditions.
- **thalesians.adiutor.config**: Configuration options for controlling the minimum enforcement level of preconditions and postconditions.

Testing
-------
The module includes a `_test()` function for testing with `doctest`.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import functools

from thalesians.adiutor.checks import check
import thalesians.adiutor.config as our_config

def conditions(pre=None, post=None, message='Condition violated', level=1):
    def decorator(func):
        # Use functools to preserve the name, docstring, etc.
        if our_config.MIN_PRECONDITION_LEVEL <= level and our_config.MIN_POSTCONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                if pre is not None:
                    check(pre(*args, **kwargs), message=lambda: message, level=level)
                retval = func(*args, **kwargs)
                if post is not None:
                    check(post(retval), message=lambda: message, level=level)
                return retval
        elif our_config.MIN_PRECONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                if pre is not None:
                    check(pre(*args, **kwargs), message=lambda: message, level=level)
                return func(*args, **kwargs)
        elif our_config.MIN_POSTCONDITION_LEVEL <= level:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # NB: No self
                retval = func(*args, **kwargs)
                if post is not None:
                    check(post(retval), message=lambda: message, level=level)
                return retval
        else:
            def wrapper(*args, **kwargs):  # NB: No self
                return func(*args, **kwargs)
        return wrapper
    return decorator

def precondition(check, message='Precondition violated', level=1):
    return conditions(pre=check, message=message, level=level)

def postcondition(check, message='Postcondition violated', level=1):
    return conditions(post=check, message=message, level=level)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

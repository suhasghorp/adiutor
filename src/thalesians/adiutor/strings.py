"""
thalesians.adiutor.strings
==========================

This module provides utilities for string manipulation and formatting. It includes functions for string sanitization, 
uniqueness checks, quoting, and structured string representation through the `ToStringHelper` class.

Key Features
------------
1. **String Sanitization**:
   - Normalize and simplify strings using `sanitize_str`.
   - Convert special characters to underscores and remove accents.

2. **Unique String Generation**:
   - Ensure uniqueness of a string within a set using `make_unique_str`.

3. **String Quoting**:
   - Quote strings with customizable characters (`enquote`).

4. **Structured String Representation**:
   - Build structured string representations for objects with the `ToStringHelper` class.

Functions
---------
### String Utilities
- **sanitize_str(raw_str)**:
  - Normalizes a string by:
    - Removing accents (using `unidecode`).
    - Converting to lowercase.
    - Replacing non-alphanumeric characters with underscores.

- **make_unique_str(raw_str, strs)**:
  - Ensures `raw_str` is unique within a given set `strs`.
  - Appends a numeric suffix if needed.

- **enquote(s, quote='"', escape=True)**:
  - Encloses a string in quotes (default: double quotes).
  - Escapes existing quotes and backslashes if `escape` is `True`.

### Class: ToStringHelper
A helper class for creating structured string representations of objects.

#### Constructor
- **`ToStringHelper(typ=None)`**:
  - Initializes the helper with an optional object type.

#### Methods
- **`set_type(typ=None)`**:
  - Sets the type name for the string representation.
  - If `typ` is an object, its class name is used.

- **`add(name, value)`**:
  - Adds a property with its name and value to the string representation.

- **`add_all_properties(o, ignore_dunders=True)`**:
  - Automatically adds all attributes of an object `o` to the string representation.
  - Ignores "dunder" (double underscore) attributes by default.

- **`to_string()`**:
  - Returns the structured string representation.

- **`__str__()`**:
  - Returns the string representation via `to_string`.

Usage
-----
### String Sanitization
    >>> from thalesians.adiutor.strings import sanitize_str
    >>> sanitize_str("Héllo, World!")
    'hello_world'

### Unique String Generation
    >>> from thalesians.adiutor.strings import make_unique_str
    >>> existing_strings = {"name", "name_1"}
    >>> make_unique_str("name", existing_strings)
    'name_2'

### Quoting Strings
    >>> from thalesians.adiutor.strings import enquote
    >>> enquote('example "string"', quote="'")
    "'example \\"string\\"'"

### Using ToStringHelper
    >>> from thalesians.adiutor.strings import ToStringHelper
    >>> obj = ToStringHelper(typ="Example")
    >>> obj.add("property1", 42).add("property2", "value")
    >>> str(obj)
    'Example(property1=42, property2="value")'

    >>> class MyClass:
    ...     def __init__(self, name, value):
    ...         self.name = name
    ...         self.value = value
    >>> obj = MyClass(name="test", value=123)
    >>> helper = ToStringHelper(obj).add_all_properties(obj)
    >>> str(helper)
    'MyClass(name="test", value=123)'

Dependencies
------------
- **unidecode**: For removing accents and normalizing strings.
- **thalesians.adiutor.checks**: For type checking and validation.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The `sanitize_str` function is useful for preparing strings for filenames, database keys, or identifiers.
- `ToStringHelper` is particularly useful for debugging or creating detailed logs of object states.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import io
import re

import thalesians.adiutor.checks as our_checks

import unidecode

def sanitize_str(raw_str):
    processed_str = raw_str
    processed_str = unidecode.unidecode(processed_str)
    processed_str = processed_str.lower()
    processed_str = re.sub(r'[_\W]+', '_', processed_str)
    return processed_str

def make_unique_str(raw_str, strs):
    processed_str = raw_str
    if processed_str in strs:
        i = 1
        candidate_str = f'{processed_str}_{i}'
        while candidate_str in strs:
            i += 1
            candidate_str = f'{processed_str}_{i}'
        processed_str = candidate_str
    return processed_str

def enquote(s, quote='"', escape=True):
    s = str(s)
    if escape: s = str(s).replace('\\', "\\\\").replace(quote, '\\' + quote)
    return quote + s + quote

class ToStringHelper(object):
    def __init__(self, typ=None):
        self.set_type(typ)
        self._properties = []
        self._str = None
        
    def set_type(self, typ=None):
        if typ is not None:
            if not our_checks.is_type(typ): typ = type(typ)
            typ = typ.__name__
        self._type_name = typ
        return self
        
    def add(self, name, value):
        self._properties.append((name, value))
        self._str = None
        return self
    
    def add_all_properties(self, o, ignore_dunders=True):
        if hasattr(o, '__dict__'):
            for prop, value in vars(o).items():
                if ignore_dunders and prop.startswith('__'): continue
                self.add(prop, value)
        return self
    
    def _should_enquote(self, o):
        return our_checks.is_string(o)
    
    def to_string(self):
        if self._str is None:
            s = io.StringIO()
            if self._type_name is not None: s.write(self._type_name)
            s.write('(')
            for i, p in enumerate(self._properties):
                if i > 0: s.write(', ')
                s.write(p[0])
                s.write('=')
                v = p[1]
                if self._should_enquote(v): s.write(enquote(v))
                else: s.write(str(v))
            s.write(')')
            self._str = s.getvalue()
        return self._str
                
    def __str__(self):
        return self.to_string()

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

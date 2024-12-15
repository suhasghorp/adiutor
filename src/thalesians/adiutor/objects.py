"""
thalesians.adiutor.objects
==========================

This module provides base classes for creating objects with customizable names and string representations. 
The main class, `Named`, is designed to give objects meaningful, identifiable names and a structured string 
representation using a helper from the `thalesians.adiutor.strings` package.

Key Features
------------
1. **Named Objects**:
   - Provides a base class (`Named`) for objects that can have a customizable or auto-generated name.
   - Automatically generates a unique name if none is provided.

2. **Custom String Representation**:
   - Uses the `ToStringHelper` utility to create structured string representations for debugging and logging.

Classes
-------
### Named
A base class for named objects with customizable names and string representations.

#### Constructor
- **`Named(name=None)`**:
  - Initializes a `Named` object.
  - If `name` is not provided, a default name is generated based on the class name and object ID.

#### Properties
- **`name`**:
  - Returns the name of the object.

#### Methods
- **`to_string_helper()`**:
  - Returns a `ToStringHelper` instance for constructing the string representation of the object.
  - By default, includes the `name` attribute.

- **`__str__()`**:
  - Returns a structured string representation of the object using `ToStringHelper`.

- **`__repr__()`**:
  - Returns the same representation as `__str__()`.

Usage
-----
### Creating a Named Object
    >>> from thalesians.adiutor.objects import Named
    >>> obj = Named(name="MyObject")
    >>> print(obj.name)
    MyObject
    >>> print(obj)
    Named(name=MyObject)

### Using the Default Name
    >>> obj = Named()
    >>> print(obj.name)
    Named_<unique_id>  # Auto-generated name based on the class and object ID

### Extending the Named Class
You can extend the `Named` class to add more attributes and include them in the string representation:
    >>> class CustomNamed(Named):
    ...     def __init__(self, name=None, value=None):
    ...         super().__init__(name)
    ...         self._value = value
    ...     
    ...     def to_string_helper(self):
    ...         return super().to_string_helper().add('value', self._value)
    >>> obj = CustomNamed(name="CustomObject", value=42)
    >>> print(obj)
    CustomNamed(name=CustomObject, value=42)

Dependencies
------------
- **thalesians.adiutor.strings.ToStringHelper**:
  - Used to build structured string representations.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The `Named` class is designed to be extended by other classes that require a structured name and 
  a customizable string representation.
- The `ToStringHelper` utility simplifies the construction of string representations by chaining 
  attribute additions.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

from thalesians.adiutor.strings import ToStringHelper

class Named(object):
    def __init__(self, name=None):
        if name is None: name = type(self).__name__ + '_' + str(id(self))
        self._name = str(name)
        self._to_string_helper_Named = None
        self._str_Named = None
    
    @property
    def name(self):
        return self._name
    
    def to_string_helper(self):
        if self._to_string_helper_Named is None:
            self._to_string_helper_Named = ToStringHelper(self).add('name', self._name)
        return self._to_string_helper_Named
    
    def __str__(self):
        if self._str_Named is None: self._str_Named = self.to_string_helper().to_string()
        return self._str_Named
        
    def __repr__(self):
        return str(self)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

"""
thalesians.adiutor.time_consts
==============================

This module defines constants for time-related calculations, expressed in terms of nanoseconds, microseconds, 
milliseconds, seconds, minutes, hours, and days. Additionally, it provides `datetime.timedelta` objects 
representing single units of time for convenience in time-based computations.

Key Features
------------
1. **Time Unit Conversion Constants**:
   - Constants for converting between nanoseconds, microseconds, milliseconds, seconds, minutes, hours, and days.

2. **Predefined `datetime.timedelta` Objects**:
   - Common time intervals like one microsecond, one millisecond, one second, one minute, one hour, and one day.

Constants
---------
### Nanosecond to Millisecond
- **`NANOSECONDS_PER_MICROSECOND`**: 1,000
- **`MICROSECONDS_PER_MILLISECOND`**: 1,000
- **`NANOSECONDS_PER_MILLISECOND`**: 1,000,000

### Millisecond to Second
- **`MILLISECONDS_PER_SECOND`**: 1,000
- **`MICROSECONDS_PER_SECOND`**: 1,000,000
- **`NANOSECONDS_PER_SECOND`**: 1,000,000,000

### Second to Minute
- **`SECONDS_PER_MINUTE`**: 60
- **`MILLISECONDS_PER_MINUTE`**: 60,000
- **`MICROSECONDS_PER_MINUTE`**: 60,000,000
- **`NANOSECONDS_PER_MINUTE`**: 60,000,000,000

### Minute to Hour
- **`MINUTES_PER_HOUR`**: 60
- **`SECONDS_PER_HOUR`**: 3,600
- **`MILLISECONDS_PER_HOUR`**: 3,600,000
- **`MICROSECONDS_PER_HOUR`**: 3,600,000,000
- **`NANOSECONDS_PER_HOUR`**: 3,600,000,000,000

### Hour to Day
- **`HOURS_PER_DAY`**: 24
- **`MINUTES_PER_DAY`**: 1,440
- **`SECONDS_PER_DAY`**: 86,400
- **`MILLISECONDS_PER_DAY`**: 86,400,000
- **`MICROSECONDS_PER_DAY`**: 86,400,000,000
- **`NANOSECONDS_PER_DAY`**: 86,400,000,000,000

### Predefined `datetime.timedelta` Objects
- **`ONE_MICROSECOND`**: `dt.timedelta(microseconds=1)`
- **`ONE_MILLISECOND`**: `dt.timedelta(milliseconds=1)`
- **`ONE_SECOND`**: `dt.timedelta(seconds=1)`
- **`ONE_MINUTE`**: `dt.timedelta(minutes=1)`
- **`ONE_HOUR`**: `dt.timedelta(hours=1)`
- **`ONE_DAY`**: `dt.timedelta(days=1)`

Usage
-----
### Using Conversion Constants
    >>> from thalesians.adiutor.time_consts import SECONDS_PER_MINUTE, MILLISECONDS_PER_SECOND
    >>> SECONDS_PER_MINUTE
    60
    >>> MILLISECONDS_PER_SECOND
    1000

### Using `datetime.timedelta` Objects
    >>> from thalesians.adiutor.time_consts import ONE_SECOND, ONE_MINUTE
    >>> import datetime as dt
    >>> dt.datetime.now() + ONE_SECOND
    # Current time + 1 second
    >>> dt.datetime.now() + ONE_MINUTE
    # Current time + 1 minute

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The constants are designed to provide clarity and avoid hardcoding time-related values in computations.
- Predefined `datetime.timedelta` objects simplify time arithmetic, making the code more readable.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import datetime as dt

NANOSECONDS_PER_MICROSECOND = 1000

MICROSECONDS_PER_MILLISECOND = 1000
NANOSECONDS_PER_MILLISECOND = 1000000  

MILLISECONDS_PER_SECOND = 1000
MICROSECONDS_PER_SECOND = 1000000
NANOSECONDS_PER_SECOND = 1000000000    

SECONDS_PER_MINUTE = 60
MILLISECONDS_PER_MINUTE = 60000
MICROSECONDS_PER_MINUTE = 60000000
NANOSECONDS_PER_MINUTE = 60000000000

MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = 3600
MILLISECONDS_PER_HOUR = 3600000
MICROSECONDS_PER_HOUR = 3600000000
NANOSECONDS_PER_HOUR = 3600000000000

HOURS_PER_DAY = 24
MINUTES_PER_DAY = 1440
SECONDS_PER_DAY = 86400
MILLISECONDS_PER_DAY = 86400000
MICROSECONDS_PER_DAY = 86400000000
NANOSECONDS_PER_DAY = 86400000000000

ONE_MICROSECOND = dt.timedelta(microseconds=1)
ONE_MILLISECOND = dt.timedelta(microseconds=1000)
ONE_SECOND = dt.timedelta(seconds=1)
ONE_MINUTE = dt.timedelta(minutes=1)
ONE_HOUR = dt.timedelta(hours=1)
ONE_DAY = dt.timedelta(days=1)

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

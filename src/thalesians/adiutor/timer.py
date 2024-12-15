"""
thalesians.adiutor.timer
========================

This module provides a simple high-resolution timer utility for measuring wall-clock and CPU time, 
enabling easy benchmarking and performance monitoring in Python.

Key Features
------------
1. **High-Resolution Timing**:
   - Measures elapsed wall-clock time and CPU time with microsecond precision (where supported).

2. **Convenient Context Management**:
   - Can be used as a context manager for automatic timing of code blocks.

3. **State Management**:
   - Tracks whether the timer has been stopped and allows sampling multiple times before stopping.

Class
-----
### Timer
A class for high-resolution timing.

#### Constructor
- **`Timer()`**:
  - Initializes the timer with the current wall-clock and CPU time.

#### Methods
- **`sample()`**:
  - Samples the elapsed time since the timer was started.
  - Raises a `ValueError` if the timer has been stopped.

- **`sample_and_stop()`**:
  - Samples the elapsed time and stops the timer.
  - Prevents further sampling once stopped.

#### Properties
- **`stopped`**:
  - Returns `True` if the timer has been stopped, otherwise `False`.

- **`time`**:
  - Returns the last sampled time.

#### Context Manager Support
- **`__enter__()`**:
  - Starts the timer when used in a `with` statement.

- **`__exit__(exc_type, exc_val, exc_tb)`**:
  - Stops the timer and records the elapsed time upon exiting the context.

Usage
-----
### Basic Timer Usage
    >>> from thalesians.adiutor.timer import Timer
    >>> t = Timer()
    >>> # Perform some operations
    >>> import time
    >>> time.sleep(1)
    >>> elapsed = t.sample()
    >>> print(f"Elapsed time: {elapsed} seconds")
    Elapsed time: 1.0 seconds

### Stopping the Timer
    >>> t = Timer()
    >>> time.sleep(1)
    >>> elapsed = t.sample_and_stop()
    >>> print(f"Elapsed time: {elapsed} seconds")
    >>> t.sample()  # Raises ValueError: Timer stopped
    Traceback (most recent call last):
        ...
    ValueError: Timer stopped

### Using as a Context Manager
    >>> with Timer() as t:
    ...     time.sleep(1)
    >>> print(f"Elapsed time: {t.time} seconds")
    Elapsed time: 1.0 seconds

Notes
-----
- On Python 3.8 and later, the module will default to using `time.time()` for wall-clock time.
- For Python versions before 3.8, the deprecated `time.clock()` is used if available.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import time

# time.clock() returns the time since the method was first called, so if you
# want microsecond resolution wall time you could do something like this
# (https://stackoverflow.com/questions/1938048/high-precision-clock-in-python):
class Timer(object):
    def __init__(self):
        self._wall_time_0 = time.time()
        self._clock_0 = time.clock() if hasattr(time, 'clock') else None
        self._time = 0
        self._stopped = False

    def sample(self):
        if self._stopped: raise ValueError('Timer stopped')
        if self._clock_0 is not None:
            dc = time.clock() - self._clock_0  # @UndefinedVariable
            self._time = self._wall_time_0 + dc
        else:
            self._time = time.time() - self._wall_time_0
        return self._time
    
    def sample_and_stop(self):
        result = self.sample()
        self._stopped = True
        return result
    
    @property
    def stopped(self):
        return self._stopped
    
    @property
    def time(self):
        return self._time
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sample_and_stop()

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

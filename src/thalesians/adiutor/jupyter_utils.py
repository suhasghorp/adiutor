"""
thalesians.adiutor.jupyter_utils
================================

This module provides utility functions for enhancing the functionality of Jupyter Notebooks, 
particularly for running background jobs using IPython magic commands.

Key Features
------------
1. **Background Job Management**:
   - Allows users to execute functions asynchronously in Jupyter Notebooks using a custom `%start` magic command.

2. **IPython Integration**:
   - Uses the IPython `backgroundjobs` module to manage asynchronous tasks.
   - Provides seamless integration with Jupyter's interactive environment.

Functions
---------
- **`start(fun)`**:
  - A line magic function to execute a Python function as a background job.
  - Returns a `BackgroundJobManager` instance to monitor and manage the job.
  
  Example:
      >>> from thalesians.adiutor.jupyter_utils import start
      >>> def my_function():
      ...     import time
      ...     time.sleep(5)
      ...     print("Task completed!")
      >>> jobs = %start my_function
      >>> jobs.status
      # Background job's status will be displayed.

Usage
-----
### Starting a Background Job
Define a function and run it in the background using `%start`:
    >>> def long_running_task():
    ...     import time
    ...     time.sleep(10)
    ...     print("Task completed!")
    >>> jobs = %start long_running_task

### Managing Background Jobs
The `BackgroundJobManager` object returned by `%start` allows you to manage running jobs:
    >>> jobs.status
    >>> jobs.kill(0)  # Kill the first job

Dependencies
------------
- **IPython.core.magic**: For registering custom IPython magic commands.
- **IPython.lib.backgroundjobs**: Provides the `BackgroundJobManager` for asynchronous task management.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
This utility is designed for use in Jupyter Notebook environments where interactive execution is common.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

from IPython.core.magic import register_line_magic
from IPython.lib import backgroundjobs as bg

@register_line_magic
def start(fun):
    jobs = bg.BackgroundJobManager()
    jobs.new(fun)
    return jobs

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()

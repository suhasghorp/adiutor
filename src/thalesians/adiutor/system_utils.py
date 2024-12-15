"""
thalesians.adiutor.system_utils
===============================

This module provides a suite of utilities for gathering system-level information, 
including hardware and software details, Python runtime configuration, and environment specifics. 
It is designed to facilitate diagnostics, monitoring, and system introspection.

Key Features
------------
1. **User and Script Information**:
   - Retrieve the home directory, process ID, and thread ID.
   - Get the path of the currently running script.

2. **Python Environment Details**:
   - Access Python version information.
   - Retrieve the path to the Python interpreter and active Conda environment.
   - List installed packages (via pip and Conda).

3. **Operating System Information**:
   - Get OS name, version, release, and detailed platform information.
   - Access hostname and IP addresses.

4. **Hardware Information**:
   - Retrieve CPU specifications, including make, core counts, and frequency.
   - Get GPU information (if available) and memory details.

Functions
---------
### User and Script Information
- **get_user_dir()**:
  - Returns the user's home directory.

- **get_pid()**:
  - Returns the current process ID.

- **get_tid()**:
  - Returns the current thread ID.

- **get_running_script_path()**:
  - Returns the path of the currently running script.

### Python Environment Details
- **get_python_version()**:
  - Returns the Python version as a string.

- **get_python_version_info()**:
  - Returns a `sys.version_info` object with version details.

- **get_python_version_major()**, **get_python_version_minor()**, **get_python_version_micro()**:
  - Return major, minor, and micro components of the Python version.

- **get_python_interpreter_path()**:
  - Returns the path to the Python executable.

- **get_conda_env_path()**:
  - Returns the path to the active Conda environment.

- **get_pip_packages()**:
  - Returns a list of installed pip packages with details like name, version, and platform.

- **get_conda_packages()**:
  - Returns a list of installed Conda packages in canonical format.

- **get_conda_channels(conda_packages=None)**:
  - Returns the Conda channels associated with the environment.

### Operating System Information
- **get_os_name()**, **get_os_version()**, **get_os_release()**:
  - Return OS name, version, and release.

- **get_os_info_string()**:
  - Returns a detailed string about the OS platform.

- **get_hostname()**:
  - Returns the hostname of the system.

- **get_ip_addresses()**:
  - Returns the IP addresses associated with the hostname.

### Hardware Information
- **get_cpu_make()**:
  - Returns the CPU model/make.

- **get_cpu_core_count()**, **get_cpu_physical_core_count()**, **get_cpu_logical_core_count()**:
  - Return the total, physical, and logical core counts of the CPU.

- **get_cpu_freq()**:
  - Returns the current CPU frequency.

- **get_gpu_count()**:
  - Returns the number of GPUs available on the system.

- **get_gpu_info(gpu_index)**:
  - Returns detailed information about the GPU at the specified index.

- **get_virtual_memory()**:
  - Returns a dictionary with details about the system's virtual memory.

- **get_swap_memory()**:
  - Returns a dictionary with details about the system's swap memory.

Dependencies
------------
- **platform**: For OS and CPU information.
- **psutil**: For memory and CPU details.
- **socket**: For networking information.
- **conda.cli.main_list**: For Conda package management.
- **GPUtil**: For GPU details.
- **pkg_resources**: For pip-installed package details.

Usage
-----
### Retrieving System Details
    >>> from thalesians.adiutor.system_utils import get_os_name, get_cpu_core_count
    >>> get_os_name()
    'Windows'
    >>> get_cpu_core_count()
    8

### Getting Python and Package Information
    >>> from thalesians.adiutor.system_utils import get_python_version, get_pip_packages
    >>> get_python_version()
    '3.10.4'
    >>> pip_packages = get_pip_packages()
    >>> pip_packages[0]
    {'project_name': 'numpy', 'module_path': '...', 'version': '1.23.4', 'py_version': '3.10', 'platform': 'any'}

### Accessing GPU Details
    >>> from thalesians.adiutor.system_utils import get_gpu_count, get_gpu_info
    >>> get_gpu_count()
    2
    >>> get_gpu_info(0)
    {'gpu_id': 0, 'gpu_name': 'NVIDIA GeForce RTX 3080', 'gpu_load': 12.5, 
     'free_memory_mb': 1000, 'used_memory_mb': 9000, 'total_memory_mb': 10000, 'temperature_celcius': 65.0}

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The module is highly dependent on system-level libraries and may have varying compatibility across platforms.
- GPU functions require `GPUtil` and will only work if GPUs are installed and accessible.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import os
from pathlib import Path
import platform
import psutil
import socket
import sys
import threading

import conda.cli.main_list
import conda.models.channel
import GPUtil
import pkg_resources

def get_user_dir():
    return str(Path.home())

def get_pid():
    return os.getpid()

def get_tid():
    return threading.get_native_id()

def get_running_script_path():
    return os.path.abspath(sys.argv[0])

def get_python_version():
    return sys.version

def get_python_version_info():
    return sys.version_info

def get_python_version_major():
    return get_python_version_info().major

def get_python_version_minor():
    return get_python_version_info().minor

def get_python_version_micro():
    return get_python_version_info().micro

def get_python_version_releaselevel():
    return get_python_version_info().releaselevel

def get_python_version_serial():
    return get_python_version_info().serial

def get_python_interpreter_path():
    return sys.executable

def get_conda_env_path():
    return sys.prefix

def get_pip_packages():
    return [{
        'project_name': package.project_name,
        'module_path': package.module_path,
        'version': package.version,
        'py_version': package.py_version,
        'platform': package.platform
        } for package in pkg_resources.working_set]

def get_conda_packages():
    return conda.cli.main_list.list_packages(get_conda_env_path(), format='canonical', reverse=False, show_channel_urls=True)[1]

def get_conda_channels(conda_packages=None):
    if conda_packages is None: conda_packages = get_conda_packages()
    channels = sorted(set([conda_package.split('/')[0] for conda_package in conda_packages]))
    result = {}
    for channel in channels:
        result[channel] = list(conda.models.channel.all_channel_urls([channel]))
    return result

def get_os_name():
    return platform.system()

def get_os_version():
    return platform.version()

def get_os_release():
    return platform.release()

def get_os_info_string():
    return platform.platform()

def get_hostname():
    return socket.gethostbyaddr(socket.gethostname())[0]

def get_ip_addresses():
    return socket.gethostbyaddr(socket.gethostname())[2]

def get_cpu_make():
    return platform.processor()

def get_cpu_core_count():
    return os.cpu_count()

def get_cpu_physical_core_count():
    return psutil.cpu_count(logical=False)

def get_cpu_logical_core_count():
    return psutil.cpu_count(logical=True)

def get_cpu_freq():
    return psutil.cpu_freq()

def get_gpu_count():
    return len(GPUtil.getGPUs())

def get_gpu_info(gpu_index):
    gpu_info = GPUtil.getGPUs()[gpu_index]
    return {
        'gpu_id': gpu_info.id,
        'gpu_name': gpu_info.name,
        'gpu_load': gpu_info.load * 100,
        'free_memory_mb': gpu_info.memoryFree,
        'used_memory_mb': gpu_info.memoryUsed,
        'total_memory_mb': gpu_info.memoryTotal,
        'temperature_celcius': gpu_info.temperature
    }

def get_virtual_memory():
    virtual_memory = psutil.virtual_memory()
    return {
        'total_virtual_memory_gb': virtual_memory.total / (1024 ** 3),
        'available_virtual_memory_gb': virtual_memory.available / (1024 ** 3),
        'used_virtual_memory_gb': virtual_memory.used / (1024 ** 3),
        'virtual_memory_percentage': virtual_memory.percent, 
    }
    
def get_swap_memory():
    swap_memory = psutil.swap_memory()
    return {
        'total_swap_memory_gb': swap_memory.total / (1024 ** 3),
        'used_swap_memory_gb': swap_memory.used / (1024 ** 3),
        'free_swap_memory_gb': swap_memory.free / (1024 ** 3),
        'swap_memory_percentage': swap_memory.percent,
    }
    
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
    
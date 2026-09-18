import sys
import os
import platform

def get_config_dir() -> str:
    # ruleid: python-no-speculative-platform-branching
    if sys.platform == "win32":
        return r"C:\Config"
    return "/etc/config"

def check_system():
    # ruleid: python-no-speculative-platform-branching
    if platform.system() == "Windows":
        return "win"
    
    # ruleid: python-no-speculative-platform-branching
    if os.name == "nt":
        return "win"

def get_standard_dir() -> str:
    # ok: python-no-speculative-platform-branching
    return "/etc/config"

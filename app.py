from cx_Freeze import setup, Executable
import sys
import os
from PySide6 import QtCore
import platform

# Determine the current platform
current_platform = platform.system().lower()

# Collect PySide6 required libraries (Qt's dynamic libraries)
pyside6_path = os.path.dirname(QtCore.__file__)

# Specify the bin folder path
bin_folder = os.path.join(os.getcwd(), 'bin')

# Collect all files from the bin folder
include_files = [
    os.path.join(pyside6_path, "plugins", "platforms"),  # Ensure platform plugins are included
    (bin_folder, "bin"),  # Include the entire bin folder
]

# Platform-specific configurations
if current_platform == "windows":
    base = "Win32GUI"
    icon = os.path.join("icon", "win", "icon.ico")
elif current_platform == "darwin":
    base = None
    icon = os.path.join("icon", "mac", "icon.icns")
else:  # Linux
    base = None
    icon = os.path.join("icon", "linux", "icon.png")

build_exe_options = {
    "packages": ["os", "sys", "PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets"],
    "include_files": include_files,
    "excludes": ["tkinter"],  # Exclude any unnecessary libraries
}

# Define the setup
setup(
    name="Youtube Downloader",
    version="2024.09.24b4",
    description="Minimalist Youtube Downloader with Qt",
    options={"build_exe": build_exe_options},
    executables=[Executable("mdu.py", base=base, icon=icon, target_name="Youtube Downloader")],
)

# Additional platform-specific setup
if current_platform == "darwin":
    from setuptools import setup

    APP = ['mdu.py']
    DATA_FILES = []
    OPTIONS = {
        'argv_emulation': True,
        'packages': ['PySide6'],
        'includes': ['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
        'iconfile': icon,
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
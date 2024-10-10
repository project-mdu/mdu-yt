from cx_Freeze import setup, Executable
import sys
import os
from PySide6 import QtCore
import platform
from src.mduyt.utils.version import appversion
# Determine the current platform
current_platform = platform.system().lower()

# Collect PySide6 required libraries (Qt's dynamic libraries)
pyside6_path = os.path.dirname(QtCore.__file__)

# Specify the bin folder path
bin_folder = os.path.join(os.getcwd(), 'bin')

# Collect platform-specific files from the bin folder
if current_platform == "windows":
    bin_include = [(os.path.join(bin_folder, 'win'), 'bin/win')]
    base = "Win32GUI"
    icon = os.path.join("icon", "win", "icon.ico")
elif current_platform == "darwin":
    bin_include = [(os.path.join(bin_folder, 'mac'), 'bin')]
    base = None
    icon = os.path.join("icon", "mac", "icon.icns")
else:  # Linux
    bin_include = [(os.path.join(bin_folder, 'linux'), 'bin')]
    base = None
    icon = os.path.join("icon", "linux", "icon.png")

# Define include_files with platform-specific bin folder
include_files = [
    os.path.join(pyside6_path, "plugins", "platforms"),  # Ensure platform plugins are included
] + bin_include

build_exe_options = {
    "packages": ["os", "sys", "PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets"],
    "include_files": include_files,
    "excludes": ["tkinter"],  # Exclude any unnecessary libraries
}

# Define the setup
setup(
    name="Youtube Downloader",
    version=appversion,
    description="Minimalist Youtube Downloader with Qt",
    options={"build_exe": build_exe_options},
    executables=[Executable("mdu.py", base=base, icon=icon, target_name="mdu")],
)

# Additional platform-specific setup for macOS
if current_platform == "darwin":
    from setuptools import setup

    APP = ['mdu.py']
    DATA_FILES = bin_include  # Include macOS-specific binaries
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

from cx_Freeze import setup, Executable
import sys
import os
from PyQt5 import QtCore
import platform
from src.mduyt.utils.version import appversion
import sys
# Determine the current platform
current_platform = platform.system().lower()

# Collect PyQt5 required libraries (Qt's dynamic libraries)
PyQt5_path = os.path.dirname(QtCore.__file__)

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
if sys.platform == "win32":
    include_files = [
        os.path.join(PyQt5_path, "Qt5", "plugins", "platforms"),  # Windows platform plugins
    ] + bin_include
elif sys.platform == "linux" or sys.platform == "darwin":  # Linux or macOS
    include_files = [
        os.path.join(PyQt5_path, "Qt", "plugins", "platforms"),  # Linux/macOS platform plugins
    ] + bin_include
else:
    raise RuntimeError("Unsupported platform")

build_exe_options = {
    "packages": ["os", "sys", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"],
    "include_files": include_files,
    "excludes": ["tkinter"],  # Exclude any unnecessary libraries
}

# Define the setup
setup(
    name="Youtube Downloader",
    version=appversion,
    description="Minimalist Youtube Downloader with Qt",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, icon=icon, target_name="mdu")],
)

# Additional platform-specific setup for macOS
if current_platform == "darwin":
    from setuptools import setup

    APP = ['mdu.py']
    DATA_FILES = bin_include  # Include macOS-specific binaries
    OPTIONS = {
        'argv_emulation': True,
        'packages': ['PyQt5'],
        'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
        'iconfile': icon,
    }

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

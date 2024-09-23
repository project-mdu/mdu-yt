from cx_Freeze import setup, Executable
import sys
import os
from PySide6 import QtCore

# Collect PySide6 required libraries (Qt's dynamic libraries)
pyside6_path = os.path.dirname(QtCore.__file__)

# Specify the bin folder path
bin_folder = os.path.join(os.getcwd(), 'bin')

# Collect all .exe and .dll files from the bin folder
include_files = [
    os.path.join(pyside6_path, "plugins", "platforms"),  # Ensure platform plugins are included
    ("app.ico", "app.ico"),  # Include the application icon
    (bin_folder, "bin"),  # Include the entire bin folder
]

# # Add all .exe and .dll files from the bin folder
# for file in os.listdir(bin_folder):
#     if file.endswith('.exe') or file.endswith('.dll'):
#         include_files.append((os.path.join(bin_folder, file), file))

build_exe_options = {
    "packages": ["os", "sys", "PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets"],
    "include_files": include_files,
    "excludes": ["tkinter"],  # Exclude any unnecessary libraries
}

# Define the setup
setup(
    name="Youtube Downloader",
    version="2024.09.23",
    description="Minimalist Youtube Downloader with Qt",
    options={"build_exe": build_exe_options},
    executables=[Executable("mdu.py", base="Win32GUI", icon="app.ico")],
)

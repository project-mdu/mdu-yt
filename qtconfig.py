import sys
import platform

def get_windows_version():
    return int(platform.version().split('.')[0])

if get_windows_version() >= 10:
    # Windows 10 or 11
    from PySide6 import QtWidgets, QtGui, QtCore
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtGui import QAction
    from PySide6.QtCore import Qt, Signal

    print("Using PySide6 for Windows 10/11")
else:
    # Windows 7, 8, or 8.1
    from PyQt5 import QtWidgets, QtGui, QtCore
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtGui import QAction
    from PyQt5.QtCore import Qt, pyqtSignal as Signal

    print("Using PyQt5 for Windows 7/8/8.1")

# Alias for maintaining compatibility
QtW = QtWidgets
QtG = QtGui
QtC = QtCore
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QFile, QTextStream
from src.gui.mainwindow import MainWindow
import src.gui.resources_rc
from src.core.downloader import Downloader


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QIcon(":/app.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
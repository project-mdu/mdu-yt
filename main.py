import sys
import os
import platform
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from src.mduyt.gui.mainwindow import MainWindow
import src.mduyt.gui.resources_rc
from src.mduyt.core.downloader import Downloader


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)  # Rename app to qt_app
    qt_app.setStyle("fusion")
    qt_app.setWindowIcon(QIcon("qrc:/icon.ico"))

    # Create and display the splash screen
    splash_pix = QPixmap(":/splash.png")  # Load the splash image
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage("Loading modules...", Qt.AlignBottom | Qt.AlignLeft, Qt.white)
    window = MainWindow()

    # Simulate a loading process (if needed)
    qt_app.processEvents()  # Ensure the splash screen is displayed

    # Hide the splash screen after the main window is ready
    splash.finish(window)

    window.show()
    sys.exit(qt_app.exec())  # Use qt_app here

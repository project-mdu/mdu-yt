import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon  # Import QIcon
from src.gui.mainwindow import MainWindow
import src.gui.resources_rc
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

       # Set application icon using resource
    app.setWindowIcon(QIcon(":/app.ico"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

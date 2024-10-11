import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTextEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, Signal

class MultipleDownloadDialog(QDialog):
    start_downloads = Signal(list)  # Signal to emit the list of URLs to download

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Multiple Download")
        self.setModal(True)
        self.resize(500, 400)  # Set an initial size for the dialog

        layout = QVBoxLayout(self)

        # Label
        self.label = QLabel("Enter URLs (one per line) or import from a text file:")
        layout.addWidget(self.label)

        # Rich Text Edit
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Buttons
        button_layout = QHBoxLayout()

        self.import_button = QPushButton("Import .txt")
        self.import_button.clicked.connect(self.import_txt)
        button_layout.addWidget(self.import_button)

        self.start_button = QPushButton("Start Download")
        self.start_button.clicked.connect(self.start_download)
        button_layout.addWidget(self.start_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def import_txt(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import URLs from Text File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read the file: {str(e)}")

    def start_download(self):
        urls = self.text_edit.toPlainText().strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            QMessageBox.warning(self, "No URLs", "Please enter at least one URL to download.")
            return

        self.start_downloads.emit(urls)
        self.accept()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = MultipleDownloadDialog()
    if dialog.exec() == QDialog.Accepted:
        print("Dialog accepted")
    else:
        print("Dialog rejected")
    sys.exit(app.exec())
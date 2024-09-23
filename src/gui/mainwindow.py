import os
import sys
import json
import threading
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QProgressBar, QLabel, QRadioButton, 
                               QComboBox, QButtonGroup, QFileDialog, QMessageBox, QTableView, 
                               QStyledItemDelegate, QStatusBar)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from src.core.downloader import Downloader

class EllipsisDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data()
        if text:
            elided_text = option.fontMetrics.elidedText(text, Qt.ElideRight, option.rect.width())
            painter.save()
            painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, elided_text)
            painter.restore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        url_layout.addWidget(self.url_input)
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        url_layout.addWidget(self.download_button)
        layout.addLayout(url_layout)

        option_layout = QHBoxLayout()
        self.video_radio = QRadioButton("Video")
        self.audio_radio = QRadioButton("Audio")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.video_radio)
        self.button_group.addButton(self.audio_radio)
        self.video_radio.setChecked(True)
        option_layout.addWidget(self.video_radio)
        option_layout.addWidget(self.audio_radio)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["wav", "mp3", "m4a", "flac"])
        self.format_combo.setEnabled(False)
        option_layout.addWidget(self.format_combo)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["720", "1080", "1440", "2160", "best"])
        option_layout.addWidget(self.resolution_combo)

        self.fps_checkbox = QRadioButton("60fps")
        option_layout.addWidget(self.fps_checkbox)
        
        option_layout.addStretch()
        layout.addLayout(option_layout)

        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Download folder:")
        folder_layout.addWidget(self.folder_label)
        self.folder_path = QLineEdit()
        self.folder_path.setText(os.path.expanduser("~/Downloads"))
        folder_layout.addWidget(self.folder_path)
        self.folder_button = QPushButton("Browse")
        self.folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_button)
        layout.addLayout(folder_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)


        # Add status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Set a message in the status bar
        self.statusBar.showMessage("Developed by Nawapon Boonjua")

        self.history_model = QStandardItemModel(0, 4, self)
        self.history_model.setHorizontalHeaderLabels(["Filename", "Type", "Path", ""])
        self.history_table = QTableView()
        self.history_table.setModel(self.history_model)
        self.history_table.setItemDelegate(EllipsisDelegate())
        self.history_table.setShowGrid(False)
        self.history_table.setSelectionBehavior(QTableView.SelectRows)
        layout.addWidget(self.history_table)
        self.history_table.horizontalHeader().setStretchLastSection(True)

        self.downloader = Downloader()
        self.downloader.signals.progress.connect(self.update_progress)
        self.downloader.signals.error.connect(self.show_error)
        self.downloader.signals.finished.connect(self.download_finished)

        self.video_radio.toggled.connect(self.toggle_format_combo)
        self.audio_radio.toggled.connect(self.toggle_format_combo)

        self.load_history()
        self.resize_history_table(None)

    def resize_history_table(self, event):
        total_width = self.history_table.width()
        column_0_width = 300  # Filename
        column_1_width = 100  # Type
        column_2_width = 300  # Path
        column_3_width = total_width - (column_0_width + column_1_width + column_2_width)  # Open File button
    
        self.history_table.setColumnWidth(0, column_0_width)
        self.history_table.setColumnWidth(1, column_1_width)
        self.history_table.setColumnWidth(2, column_2_width)
        self.history_table.setColumnWidth(3, max(column_3_width, 50)) 
    @Slot()
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_path.setText(folder)

    @Slot()
    def toggle_format_combo(self):
        is_audio = self.audio_radio.isChecked()
        self.format_combo.setEnabled(is_audio)  # Enable format combo for audio
        self.resolution_combo.setEnabled(not is_audio) 

    @Slot()
    def start_download(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL")
            return

        download_dir = self.folder_path.text()
        if not os.path.isdir(download_dir):
            QMessageBox.warning(self, "Error", "Invalid download directory")
            return

        self.download_button.setEnabled(False)
        self.status_label.setText("Starting download...")
        self.progress_bar.setValue(0)

        is_audio = self.audio_radio.isChecked()
        audio_format = self.format_combo.currentText() if is_audio else None
        resolution = self.resolution_combo.currentText()
        fps = "60" if self.fps_checkbox.isChecked() else None

        thread = threading.Thread(target=self.downloader.download, 
                                  args=(url, is_audio, audio_format, resolution, fps, download_dir), 
                                  daemon=True)
        thread.start()

    @Slot(float, str, str, str)
    def update_progress(self, progress, file_size, download_speed, eta):
        self.progress_bar.setValue(int(progress))
        status = f"Downloading: {progress:.1f}%"
        if file_size:
            status += f" | Size: {file_size}"
        if download_speed:
            status += f" | Speed: {download_speed}"
        if eta:
            status += f" | ETA: {eta}"
        self.status_label.setText(status)

    @Slot(str)
    def show_error(self, error):
        self.status_label.setText(f"Error: {error}")
        self.download_button.setEnabled(True)
        QMessageBox.critical(self, "Error", error)

    @Slot(str, str, str)
    def download_finished(self, filename, file_path, file_type):
        self.status_label.setText("Download completed!")
        self.download_button.setEnabled(True)
        QMessageBox.information(self, "Success", "Download completed successfully!")
        self.add_to_history(filename, file_path, file_type)

    def add_to_history(self, filename, file_path, file_type):
        row = self.history_model.rowCount()
        self.history_model.insertRow(row)

        filename_item = QStandardItem(filename)
        file_type_item = QStandardItem(file_type)
        file_path_item = QStandardItem(file_path)

        filename_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        file_type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        file_path_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.history_model.setItem(row, 0, filename_item)
        self.history_model.setItem(row, 1, file_type_item)
        self.history_model.setItem(row, 2, file_path_item)

        dark_color_even = QColor(40, 40, 40)
        dark_color_odd = QColor(30, 30, 30)

        if row % 2 == 0:
            filename_item.setBackground(QBrush(dark_color_even))
            file_type_item.setBackground(QBrush(dark_color_even))
            file_path_item.setBackground(QBrush(dark_color_even))
        else:
            filename_item.setBackground(QBrush(dark_color_odd))
            file_type_item.setBackground(QBrush(dark_color_odd))
            file_path_item.setBackground(QBrush(dark_color_odd))

        open_button = QPushButton("...")
        open_button.setFixedHeight(20)
        open_button.clicked.connect(lambda: self.open_file_location(file_path))
        self.history_table.setIndexWidget(self.history_model.index(row, 3), open_button)
        self.history_table.setRowHeight(row, 30)
        self.history_table.resizeRowsToContents()
        self.history_table.setShowGrid(False)
        self.save_history()

    def open_file_location(self, file_path):
        if sys.platform == "win32":
            os.startfile(os.path.dirname(file_path))
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, os.path.dirname(file_path)])

    def save_history(self):
        history = []
        for row in range(self.history_model.rowCount()):
            history.append({
                "filename": self.history_model.item(row, 0).text(),
                "file_type": self.history_model.item(row, 1).text(),
                "file_path": self.history_model.item(row, 2).text()
            })
        
        with open("download_history.json", "w") as f:
            json.dump(history, f)

    def load_history(self):
        try:
            with open("download_history.json", "r") as f:
                history = json.load(f)
            
            for item in history:
                self.add_to_history(item["filename"], item["file_path"], item["file_type"])
        except FileNotFoundError:
            pass

import os
import sys
import json
import threading
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QProgressBar, QLabel, QRadioButton, 
                               QComboBox, QButtonGroup, QFileDialog, QMessageBox, QListView, 
                               QStyledItemDelegate, QStatusBar, QStyle, QMenu)
from PySide6.QtCore import Qt, Slot, QSize, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPalette, QColor, QAction
from src.core.downloader import Downloader

def normalize_path(path):
    return path.replace(os.sep, '/')

class HistoryItemWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.path_label = QLabel(normalize_path(data['path']))
        icon = QIcon(self.get_icon_path(data['file_type']))
        self.icon_label = QLabel()
        self.icon_label.setPixmap(icon.pixmap(QSize(32, 32)))
        layout.addWidget(self.icon_label)

        info_layout = QVBoxLayout()
        self.filename_label = QLabel(data['filename'])
        self.filename_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self.filename_label)

        self.path_label = QLabel(data['path'])
        self.path_label.setStyleSheet("color: gray;")
        info_layout.addWidget(self.path_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        self.setObjectName("historyItem")
        self.filename_label.setObjectName("filenameLabel")
        self.path_label.setObjectName("pathLabel")

    def get_icon_path(self, file_type):
        if file_type == 'audio':
            return ":/audio.ico"
        elif file_type == 'video':
            return ":/vid.ico"
        else:
            return ":/file.ico"

class HistoryDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alt_color1 = QColor(53, 53, 53)  # Darker gray
        self.alt_color2 = QColor(45, 45, 45)  # Slightly lighter gray

    def paint(self, painter, option, index):
        if index.row() % 2 == 0:
            painter.fillRect(option.rect, self.alt_color1)
        else:
            painter.fillRect(option.rect, self.alt_color2)

        if not self.parent().indexWidget(index):
            data = index.data(Qt.UserRole)
            if data:
                widget = HistoryItemWidget(data, self.parent())
                self.parent().setIndexWidget(index, widget)

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(42, 130, 218))

    def sizeHint(self, option, index):
        return QSize(0, 50)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon(":/app.ico"))

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
        self.folder_path.setText(normalize_path(os.path.expanduser("~/Downloads")))
        folder_layout.addWidget(self.folder_path)
        self.folder_button = QPushButton("Browse")
        self.folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_button)
        layout.addLayout(folder_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Developed by Nawapon Boonjua")

        self.history_model = QStandardItemModel()
        self.history_list = QListView()
        self.history_list.setModel(self.history_model)
        self.history_list.setItemDelegate(HistoryDelegate(self.history_list))
        self.history_list.setUniformItemSizes(False)
        self.history_list.setSpacing(2)
        self.history_list.doubleClicked.connect(self.open_file_location)
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        self.history_list.setStyleSheet("""
            QListView {
                background-color: #2b2b2b;
                border: none;
            }
            QListView::item {
                border: none;
                padding: 2px;
            }
            QListView::item:selected {
                background-color: #2a82da;
                color: white;
            }
        """)
        layout.addWidget(self.history_list)

        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)
        layout.addWidget(self.clear_history_button)

        self.downloader = Downloader()
        self.downloader.signals.progress.connect(self.update_progress)
        self.downloader.signals.error.connect(self.show_error)
        self.downloader.signals.finished.connect(self.download_finished)
        self.video_radio.toggled.connect(self.toggle_format_combo)
        self.audio_radio.toggled.connect(self.toggle_format_combo)

        self.load_history()

    @Slot()
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_path.setText(normalize_path(folder))

    @Slot()
    def toggle_format_combo(self):
        is_audio = self.audio_radio.isChecked()
        self.format_combo.setEnabled(is_audio)
        self.resolution_combo.setEnabled(not is_audio) 

    @Slot()
    def start_download(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a valid URL")
            return

        download_dir = normalize_path(self.folder_path.text())
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
        self.add_to_history(filename, normalize_path(file_path), file_type)

    def add_to_history(self, filename, file_path, file_type):
        item = QStandardItem()
        file_extension = os.path.splitext(filename)[1].lower()
        is_audio = file_extension in ['.wav', '.mp3', '.flac', '.m4a'] or file_type == 'audio'
        item.setData({
            'filename': os.path.basename(filename),
            'path': os.path.dirname(normalize_path(file_path)),
            'file_type': 'audio' if is_audio else 'video'
        }, Qt.UserRole)
        self.history_model.insertRow(0, item)
        self.save_history()

    def open_file_location(self, index):
        data = index.data(Qt.UserRole)
        if data:
            file_path = normalize_path(os.path.join(data['path'], data['filename']))
            if sys.platform == "win32":
                os.startfile(os.path.dirname(file_path))
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, os.path.dirname(file_path)])

    def save_history(self):
        history = []
        for row in range(self.history_model.rowCount()):
            item_data = self.history_model.item(row).data(Qt.UserRole)
            history.append(item_data)
        
        with open("download_history.json", "w") as f:
            json.dump(history, f)

    def load_history(self):
        try:
            with open("download_history.json", "r") as f:
                history = json.load(f)
            
            for item in history:
                list_item = QStandardItem()
                list_item.setData(item, Qt.UserRole)
                self.history_model.appendRow(list_item)
        except FileNotFoundError:
            pass

    @Slot()
    def clear_history(self):
        reply = QMessageBox.question(self, 'Clear History',
                                     'Are you sure you want to clear the download history?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.history_model.clear()
            if os.path.exists("download_history.json"):
                os.remove("download_history.json")
            self.status_label.setText("History cleared")

    
    @Slot(QPoint)
    def show_context_menu(self, position):
        index = self.history_list.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu(self)
        open_action = QAction("Open File", self)
        open_action.triggered.connect(lambda: self.open_file(index))
        menu.addAction(open_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_item(index))
        menu.addAction(delete_action)

        menu.exec_(self.history_list.viewport().mapToGlobal(position))

    def open_file(self, index):
        data = index.data(Qt.UserRole)
        if data:
            file_path = normalize_path(os.path.join(data['path'], data['filename']))
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])

    def delete_item(self, index):
        reply = QMessageBox.question(self, 'Delete Item',
                                     'Are you sure you want to delete this item from the history?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.history_model.removeRow(index.row())
            self.save_history()
            self.status_label.setText("Item deleted from history")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    app.setStyleSheet("""
        QToolTip { 
            color: #ffffff; 
            background-color: #2a82da; 
            border: 1px solid white; 
        }
        QWidget {
            font-size: 11px;
        }
        QListView::item:selected {
            background-color: #2a82da;
        }
    """)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
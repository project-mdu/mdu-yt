import os
import sys
import json
import threading
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, Qt, QModelIndex, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication
from src.core.downloader import Downloader
from src.core.updater import GitHubUpdater
import src.gui.resources_rc

def normalize_path(path):
    return QUrl(path).toLocalFile()

class HistoryModel(QAbstractListModel):
    FilenameRole = Qt.UserRole + 1
    PathRole = Qt.UserRole + 2
    IconRole = Qt.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._history)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            item = self._history[index.row()]
            if role == self.FilenameRole:
                return item['filename']
            elif role == self.PathRole:
                return item['path']
            elif role == self.IconRole:
                return self.get_icon_path(item['file_type'])
        return None

    def roleNames(self):
        return {
            self.FilenameRole: b'filename',
            self.PathRole: b'path',
            self.IconRole: b'icon'
        }

    def get_icon_path(self, file_type):
        if file_type == 'audio':
            return "qrc:/audio.ico"
        elif file_type == 'video':
            return "qrc:/vid.ico"
        else:
            return "qrc:/file.ico"

    def add_item(self, filename, file_path, file_type):
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._history.insert(0, {
            'filename': filename,
            'path': file_path,
            'file_type': file_type
        })
        self.endInsertRows()
        self.save_history()

    def clear(self):
        self.beginResetModel()
        self._history.clear()
        self.endResetModel()
        self.save_history()

    def save_history(self):
        with open("download_history.json", "w", encoding="utf-8") as f:
            json.dump(self._history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        try:
            with open("download_history.json", "r", encoding="utf-8") as f:
                self._history = json.load(f)
            self.modelReset.emit()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error decoding JSON")

class Backend(QObject):
    updateProgress = Signal(float, str, str, str)
    showError = Signal(str)
    downloadFinished = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.downloader = Downloader()
        self.downloader.signals.progress.connect(self.update_progress)
        self.downloader.signals.error.connect(self.show_error)
        self.downloader.signals.finished.connect(self.download_finished)
        self._history_model = HistoryModel()
        self._history_model.load_history()
        self.updater = GitHubUpdater("2024.09.24b4")

    @Property(QObject, constant=True)
    def historyModel(self):
        return self._history_model

    @Property(str, constant=True)
    def default_download_path(self):
        return QUrl.fromLocalFile(os.path.expanduser("~/Downloads")).toString()

    @Slot(str, result=str)
    def normalize_path(self, path):
        return normalize_path(path)

    @Slot(str, bool, str, str, str, str)
    def start_download(self, url, is_audio, audio_format, resolution, fps, download_dir):
        if not url:
            self.showError.emit("Please enter a valid URL")
            return

        download_dir = normalize_path(download_dir)
        if not os.path.isdir(download_dir):
            self.showError.emit("Invalid download directory")
            return

        thread = threading.Thread(target=self.downloader.download, 
                                  args=(url, is_audio, audio_format, resolution, fps, download_dir), 
                                  daemon=True)
        thread.start()

    @Slot(float, str, str, str)
    def update_progress(self, progress, file_size, download_speed, eta):
        self.updateProgress.emit(progress, file_size, download_speed, eta)

    @Slot(str)
    def show_error(self, error):
        self.showError.emit(error)

    @Slot(str, str, str)
    def download_finished(self, filename, file_path, file_type):
        self.downloadFinished.emit(filename, file_path, file_type)
        self._history_model.add_item(filename, file_path, file_type)

    @Slot(str, str)
    def open_file_location(self, path, filename):
        file_path = os.path.join(path, filename)
        if sys.platform == "win32":
            os.startfile(os.path.dirname(file_path))
        elif sys.platform == "darwin":
            os.system(f"open -R '{file_path}'")
        else:
            os.system(f"xdg-open '{os.path.dirname(file_path)}'")

    @Slot()
    def clear_history(self):
        self._history_model.clear()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)
    
    engine.load(QUrl.fromLocalFile("src/gui/qml/main.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())
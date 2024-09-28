import sys
import os
import asyncio
import aiohttp
from urllib.parse import urlparse
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QProgressBar, QLabel, QFileDialog, QSpinBox
from PySide6.QtCore import Qt, QObject, Signal, Slot, QThread

class DownloadWorker(QObject):
    progress_updated = Signal(int)
    download_complete = Signal()
    error_occurred = Signal(str)

    def __init__(self, url, num_connections, save_path):
        super().__init__()
        self.url = url
        self.num_connections = num_connections
        self.save_path = save_path

    async def download_chunk(self, session, start, end, filename, chunk_number):
        headers = {'Range': f'bytes={start}-{end}'}
        chunk_size = end - start + 1
        
        try:
            async with session.get(self.url, headers=headers) as response:
                with open(f"{filename}.part{chunk_number}", "wb") as f:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.progress_updated.emit(len(chunk))
        except Exception as e:
            self.error_occurred.emit(str(e))

    async def parallel_download(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(self.url) as response:
                    file_size = int(response.headers.get('Content-Length', 0))

            if file_size == 0:
                self.error_occurred.emit("Unable to determine file size.")
                return

            chunk_size = file_size // self.num_connections
            filename = os.path.join(self.save_path, os.path.basename(urlparse(self.url).path))

            tasks = []
            for i in range(self.num_connections):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < self.num_connections - 1 else file_size - 1
                task = asyncio.create_task(self.download_chunk(aiohttp.ClientSession(), start, end, filename, i))
                tasks.append(task)

            await asyncio.gather(*tasks)

            with open(filename, "wb") as outfile:
                for i in range(self.num_connections):
                    chunk_file = f"{filename}.part{i}"
                    with open(chunk_file, "rb") as infile:
                        outfile.write(infile.read())
                    os.remove(chunk_file)

            self.download_complete.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def start_download(self):
        asyncio.run(self.parallel_download())

class DownloadDialog(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Parallel Downloader')
        self.setGeometry(300, 300, 500, 200)

        layout = QVBoxLayout()

        url_layout = QHBoxLayout()
        url_label = QLabel('URL:')
        self.url_input = QLineEdit(self.url)
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        connections_layout = QHBoxLayout()
        connections_label = QLabel('Connections:')
        self.connections_input = QSpinBox()
        self.connections_input.setRange(1, 256)
        self.connections_input.setValue(16)
        connections_layout.addWidget(connections_label)
        connections_layout.addWidget(self.connections_input)
        layout.addLayout(connections_layout)

        self.path_button = QPushButton('Select Save Location')
        self.path_button.clicked.connect(self.select_save_path)
        layout.addWidget(self.path_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel('Ready to download')
        layout.addWidget(self.status_label)

        self.download_button = QPushButton('Start Download')
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

        self.save_path = os.path.expanduser("~/Downloads")

    def select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Save Location")
        if self.save_path:
            self.path_button.setText(f"Save to: {self.save_path}")

    def start_download(self):
        url = self.url_input.text()
        num_connections = self.connections_input.value()

        self.download_thread = QThread()
        self.worker = DownloadWorker(url, num_connections, self.save_path)
        self.worker.moveToThread(self.download_thread)

        self.worker.progress_updated.connect(self.update_progress)
        self.worker.download_complete.connect(self.download_finished)
        self.worker.error_occurred.connect(self.handle_error)

        self.download_thread.started.connect(self.worker.start_download)
        self.download_thread.start()

        self.download_button.setEnabled(False)
        self.status_label.setText('Downloading...')

    @Slot(int)
    def update_progress(self, chunk_size):
        current_value = self.progress_bar.value()
        self.progress_bar.setValue(current_value + chunk_size)

    @Slot()
    def download_finished(self):
        self.status_label.setText('Download completed!')
        self.download_button.setEnabled(True)
        self.download_thread.quit()
        self.download_thread.wait()

    @Slot(str)
    def handle_error(self, error_message):
        self.status_label.setText(f'Error: {error_message}')
        self.download_button.setEnabled(True)
        self.download_thread.quit()
        self.download_thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    dialog = DownloadDialog(url)
    dialog.show()
    sys.exit(app.exec())
import sys
import re
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal

def get_video_duration(input_file):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout)

class FFmpegThread(QThread):
    progress_update = pyqtSignal(float)
    conversion_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, input_file, output_file, duration):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.duration = duration

    def run(self):
        cmd = [
            "ffmpeg", "-y",
            "-i", self.input_file,
            "-c:v", "hevc_amf",
            "-c:a", "aac",
            "-b:v", "20M",
            "-preset", "ultrafast",
            "-strict", "experimental",
            self.output_file
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            for line in process.stdout:
                matches = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                if matches:
                    hours, minutes, seconds = map(float, matches.groups())
                    time_in_secs = hours * 3600 + minutes * 60 + seconds
                    progress_percentage = min(100, time_in_secs / self.duration * 100)
                    self.progress_update.emit(progress_percentage)

            process.wait()
            self.conversion_complete.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FFmpeg GUI")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        input_layout = QHBoxLayout()
        self.input_file_edit = QLineEdit()
        input_browse_button = QPushButton("Browse")
        input_browse_button.clicked.connect(self.browse_input_file)
        input_layout.addWidget(QLabel("Input File:"))
        input_layout.addWidget(self.input_file_edit)
        input_layout.addWidget(input_browse_button)
        layout.addLayout(input_layout)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

    def browse_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if file_name:
            self.input_file_edit.setText(file_name)

    def start_conversion(self):
        input_file = self.input_file_edit.text()
        if not input_file:
            self.status_label.setText("Please select an input file.")
            return

        output_file = os.path.expanduser(f"{input_file}_converted.mp4")
        
        try:
            duration = get_video_duration(input_file)
            self.ffmpeg_thread = FFmpegThread(input_file, output_file, duration)
            self.ffmpeg_thread.progress_update.connect(self.update_progress)
            self.ffmpeg_thread.conversion_complete.connect(self.conversion_completed)
            self.ffmpeg_thread.error_occurred.connect(self.error_occurred)
            self.ffmpeg_thread.start()

            self.convert_button.setEnabled(False)
            self.status_label.setText("Converting...")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def update_progress(self, value):
        self.progress_bar.setValue(int(value))

    def conversion_completed(self):
        self.status_label.setText("Conversion completed successfully!")
        self.convert_button.setEnabled(True)

    def error_occurred(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.convert_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
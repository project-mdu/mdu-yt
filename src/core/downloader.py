import os
import re
import subprocess
import sys
import platform
import shutil
from PySide6.QtCore import QObject, Signal
from env import bin

class DownloaderSignals(QObject):
    progress = Signal(float, str, str, str)
    error = Signal(str)
    finished = Signal(str, str, str)  # filename, file_path, file_type

class Downloader(QObject):
    def __init__(self):
        super().__init__()
        self.signals = DownloaderSignals()
        self.system = platform.system().lower()
        self.workdir = self.get_workdir()
        self.yt_dlp_binary = self.get_yt_dlp_binary()

    def get_workdir(self):
        if self.system == 'windows':
            return os.path.join(bin, 'win')
        elif self.system == 'darwin':
            return os.path.join(bin, 'mac')
        elif self.system == 'linux':
            return '/usr/local/bin'  # Default location for user-installed binaries
        else:
            raise OSError(f"Unsupported operating system: {self.system}")

    def get_yt_dlp_binary(self):
        if self.system == 'windows':
            return os.path.join(self.workdir, 'yt-dlp.exe')
        elif self.system == 'darwin':
            return os.path.join(self.workdir, 'yt-dlp')
        elif self.system == 'linux':
            return self.get_linux_binary()
        else:
            raise OSError(f"Unsupported operating system: {self.system}")

    def get_linux_binary(self):
        # Check if yt-dlp is already installed
        if shutil.which('yt-dlp'):
            return 'yt-dlp'
        
        # If not installed, try to install it
        package_managers = [
            ('apt-get', 'apt install -y yt-dlp'),
            ('pacman', 'pacman -S --noconfirm yt-dlp'),
            ('dnf', 'dnf install -y yt-dlp'),
            ('yum', 'yum install -y yt-dlp'),
            ('zypper', 'zypper install -y yt-dlp')
        ]

        for pm, install_cmd in package_managers:
            if shutil.which(pm):
                try:
                    subprocess.run(['sudo', pm, 'update'], check=True)
                    subprocess.run(['sudo'] + install_cmd.split(), check=True)
                    return 'yt-dlp'
                except subprocess.CalledProcessError:
                    print(f"Failed to install yt-dlp using {pm}")

        # If installation failed, use the bundled binary
        print("Using bundled yt-dlp binary")
        return os.path.join(bin, 'linux', 'yt-dlp')

    def download(self, url, is_audio, audio_format, resolution, fps, download_dir):
        try:
            # Construct the command
            cmd = [self.yt_dlp_binary, url, '--newline']
            
            # Use the download_dir parameter for the output directory
            cmd.extend(['-P', download_dir])
            
            # Add output template to remove video ID from filename
            cmd.extend(['--output', '%(title)s.%(ext)s'])
            
            if is_audio:
                cmd.extend(['-x', '--audio-format', audio_format])
            else:
                # Construct video format string based on resolution
                format_string = f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                cmd.extend(['-f', format_string])
                if fps:
                    cmd.append(f'--fps={fps}')

            # Run the subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if self.system == 'windows' else 0
            )
            
            filename = None
            for line in process.stdout:
                if '[download]' in line:
                    self.parse_progress(line)
                elif 'ERROR:' in line:
                    self.signals.error.emit(line.strip())
                elif '[ExtractAudio] Destination:' in line or '[Merger] Merging formats into' in line:
                    filename = os.path.basename(line.split('"')[-2]) if '"' in line else line.split(':')[-1].strip()

            process.wait()
            if process.returncode != 0:
                self.signals.error.emit(f"yt-dlp exited with code {process.returncode}")
            else:
                if not filename:
                    filename = self.get_last_modified_file(download_dir)
                file_path = os.path.join(download_dir, filename)
                file_type = "Audio" if is_audio else "Video"
                self.signals.finished.emit(filename, file_path, file_type)
        except Exception as e:
            self.signals.error.emit(str(e))

    def parse_progress(self, line):
        progress = 0
        file_size = ""
        download_speed = ""
        eta = ""

        match = re.search(r'(\d+(?:\.\d+)?)%', line)
        if match:
            progress = float(match.group(1))

        size_match = re.search(r'of\s+(\S+)', line)
        if size_match:
            file_size = size_match.group(1)

        speed_match = re.search(r'at\s+(\S+)', line)
        if speed_match:
            download_speed = speed_match.group(1)

        eta_match = re.search(r'ETA\s+(\S+)', line)
        if eta_match:
            eta = eta_match.group(1)

        self.signals.progress.emit(progress, file_size, download_speed, eta)

    def get_last_modified_file(self, directory):
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            return None
        return max(files, key=os.path.getmtime)
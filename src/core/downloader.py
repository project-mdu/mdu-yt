import os
import re
import subprocess
import sys
import platform
import shutil
from PySide6.QtCore import QObject, Signal
from env import bin

class DownloaderSignals(QObject):
    progress = Signal(float, str, str, str, int, int)
    file_downloaded = Signal(str, str, str)
    finished = Signal()
    error = Signal(str)

class Downloader(QObject):
    def __init__(self):
        super().__init__()
        self.system = platform.system().lower()
        self.workdir = self.get_workdir()
        self.yt_dlp_binary = self.get_yt_dlp_binary()
        self.signals = DownloaderSignals()
        self.process = None
        self.stop_flag = False

    def get_workdir(self):
        if self.system == 'windows':
            return os.path.join(bin, 'bin', 'win')
        elif self.system == 'darwin':
            return os.path.join(bin, 'bin', 'mac')
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

    def download(self, url, is_audio, audio_format, resolution, fps, download_dir, is_playlist, with_thumbnail):
        try:
            self.stop_flag = False
            # Construct the command
            cmd = [self.yt_dlp_binary, url, '--newline']

            # Use the download_dir parameter for the output directory
            cmd.extend(['-P', download_dir])

            # Add output template to remove video ID from filename
            if is_playlist:
                cmd.extend(['--output', '%(playlist_title)s/%(title)s.%(ext)s'])
            else:
                cmd.extend(['--output', '%(title)s.%(ext)s'])

            if with_thumbnail:
                cmd.extend(["--embed-thumbnail", "--embed-metadata"])

            if is_audio:
                cmd.extend(['-x', '--audio-format', audio_format])
            else:
                # Construct video format string based on resolution
                format_string = f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                cmd.extend(['-f', format_string])
                if fps:
                    cmd.append(f'--fps={fps}')

            if is_playlist:
                cmd.append('--yes-playlist')
            else:
                cmd.append('--no-playlist')

            # Run the subprocess
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if self.system == 'windows' else 0
            )

            current_item = 0
            total_items = 1
            for line in self.process.stdout:
                if self.stop_flag:
                    self.process.terminate()
                    self.signals.error.emit("Download stopped by user")
                    return

                if '[download] Downloading item' in line:
                    match = re.search(r'item (\d+) of (\d+)', line)
                    if match:
                        current_item = int(match.group(1))
                        total_items = int(match.group(2))
                elif '[download]' in line:
                    progress, file_size, download_speed, eta = self.parse_progress(line)
                    self.signals.progress.emit(progress, file_size, download_speed, eta, current_item, total_items)
                elif '[ExtractAudio] Destination:' in line or '[Merger] Merging formats into' in line:
                    filename = os.path.basename(line.split('"')[-2]) if '"' in line else line.split(':')[-1].strip()
                    file_path = os.path.join(download_dir, filename)
                    file_type = "Audio" if is_audio else "Video"
                    self.signals.file_downloaded.emit(filename, file_path, file_type)

            self.process.wait()
            if self.process.returncode != 0 and not self.stop_flag:
                self.signals.error.emit(f"yt-dlp exited with code {self.process.returncode}")
            elif not self.stop_flag:
                self.signals.finished.emit()

        except Exception as e:
            self.signals.error.emit(str(e))

    def stop(self):
        self.stop_flag = True
        if self.process:
            self.process.terminate()

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

        return progress, file_size, download_speed, eta
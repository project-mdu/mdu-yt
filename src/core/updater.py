import os
import sys
import requests
from packaging import version
import tempfile
import zipfile
import shutil
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal

class UpdaterSignals(QObject):
    update_available = Signal(str)
    update_progress = Signal(int)
    update_completed = Signal()
    update_error = Signal(str)

class GitHubUpdater:
    def __init__(self, current_version):
        self.current_version = current_version
        self.api_url = "https://api.github.com/repos/Rinechxn/mdu-yt/releases/latest"
        self.signals = UpdaterSignals()

    def check_for_updates(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            if version.parse(latest_version) > version.parse(self.current_version):
                self.signals.update_available.emit(latest_version)
                return latest_release
            else:
                return None
        except requests.RequestException as e:
            self.signals.update_error.emit(f"Error checking for updates: {str(e)}")
            return None

    def download_and_install_update(self, release):
        try:
            asset = next((asset for asset in release['assets'] if asset['name'].endswith('.zip')), None)
            if not asset:
                raise ValueError("No suitable asset found in the release")

            download_url = asset['browser_download_url']
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                self._download_file(download_url, zip_path)
                self._extract_update(zip_path)
                self._replace_current_executable()
                
            self.signals.update_completed.emit()
        except Exception as e:
            self.signals.update_error.emit(f"Error during update: {str(e)}")

    def _download_file(self, url, local_path):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(local_path, 'wb') as file:
            downloaded = 0
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded += len(data)
                progress = int((downloaded / total_size) * 100)
                self.signals.update_progress.emit(progress)

    def _extract_update(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zip_path))

    def _replace_current_executable(self):
        if getattr(sys, 'frozen', False):
            # Running as a bundled executable
            current_exe = sys.executable
            new_exe = os.path.join(os.path.dirname(current_exe), "new_version.exe")
            os.rename(current_exe, current_exe + ".old")
            os.rename(new_exe, current_exe)
        else:
            # Running as a script, just overwrite the script files
            script_dir = os.path.dirname(os.path.abspath(__file__))
            for root, dirs, files in os.walk(script_dir):
                for file in files:
                    if file.endswith('.py'):
                        new_file = os.path.join(root, "new_" + file)
                        if os.path.exists(new_file):
                            os.replace(new_file, os.path.join(root, file))
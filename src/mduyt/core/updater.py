import os
import sys
import requests
from packaging import version
import tempfile
import zipfile
import shutil
import subprocess
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal


class UpdaterSignals(QObject):
    update_available = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    update_completed = pyqtSignal()
    update_error = pyqtSignal(str)

class GitHubUpdater:
    def __init__(self, current_version, is_portable=False):
        self.current_version = current_version
        self.is_portable = is_portable
        self.api_url = "https://api.github.com/repos/project-mdu/mdu-yt/releases/latest"
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
            if self.is_portable:
                asset = next((asset for asset in release['assets'] if asset['name'].endswith('.zip')), None)
            else:
                asset = next((asset for asset in release['assets'] if asset['name'].endswith('.exe')), None)

            if not asset:
                raise ValueError("No suitable asset found in the release")

            download_url = asset['browser_download_url']
            with tempfile.TemporaryDirectory() as temp_dir:
                local_path = os.path.join(temp_dir, asset['name'])
                self._download_file(download_url, local_path)

                if self.is_portable:
                    self._update_portable(local_path)
                else:
                    self._run_installer(local_path)

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

    def _update_portable(self, zip_path):
        app_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(app_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

        # Restart the application
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _run_installer(self, installer_path):
        # Run the Inno Setup installer with silent install flags
        subprocess.run(installer_path, check=True)

        # After installation, we need to exit the current application
        # The new version will be launched by the installer
        sys.exit(0)

# scripts/python/autobuild.py

import subprocess
import os
import zipfile
import json
import sys
from datetime import datetime
import platform

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(f"Error message: {stderr.decode()}")
        exit(1)
    return stdout.decode()

def create_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

def create_buildnumber_json(version, build_id):
    build_info = {
        "version": version,
        "time": datetime.now().isoformat(),
        "build_id": build_id
    }
    with open("buildnumber.json", "w") as f:
        json.dump(build_info, f, indent=2)

def get_platform_specific_paths():
    system = platform.system().lower()
    if system == "windows":
        build_dir = os.path.join(os.getcwd(), "build", "exe.win-amd64-3.12")
        inno_setup_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
        return build_dir, inno_setup_path
    elif system == "darwin":
        build_dir = os.path.join(os.getcwd(), "build", "Youtube Downloader.app")
        return build_dir, None
    elif system == "linux":
        build_dir = os.path.join(os.getcwd(), "build", "exe.linux-x86_64-3.12")
        return build_dir, None
    else:
        print(f"Unsupported platform: {system}")
        exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/python/autobuild.py [windows|mac|linux]")
        exit(1)

    target_platform = sys.argv[1].lower()
    if target_platform not in ["windows", "mac", "linux"]:
        print("Invalid platform. Choose 'windows', 'mac', or 'linux'.")
        exit(1)

    # Change to the project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # Create buildnumber.json
    print("Creating buildnumber.json...")
    version = "1.0.0"  # You may want to get this from a config file or as a parameter
    build_id = datetime.now().strftime("%Y%m%d%H%M%S")
    create_buildnumber_json(version, build_id)

    # Run app.py build
    print("Running app.py build...")
    if target_platform == "mac":
        run_command("python app.py py2app")
    else:
        run_command("python app.py build")

    # Get platform-specific paths
    build_dir, inno_setup_path = get_platform_specific_paths()

    # Create a zip file with timestamp
    print("Creating zip file...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join("build", "portable", f"youtube-downloader-portable_{target_platform}_{timestamp}.zip")
    create_zip(build_dir, zip_filename)
    print(f"Created zip file: {zip_filename}")

    # Run platform-specific installer creation
    if target_platform == "windows" and inno_setup_path:
        if not os.path.exists(inno_setup_path):
            print(f"Inno Setup not found at {inno_setup_path}")
            print("Please install Inno Setup or update the path in the script.")
        else:
            print("Running Inno Setup...")
            run_command(f'"{inno_setup_path}" scripts/installer/makeinstall.iss')
    elif target_platform == "mac":
        print("macOS .app bundle created.")
        # Add commands here if you want to create a .dmg file
    elif target_platform == "linux":
        print("Creating Linux package...")
        # Add commands to create a Linux package
        # This might involve using tools like fpm or creating a .deb package

    print("Build process completed successfully!")

if __name__ == "__main__":
    main()
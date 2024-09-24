import subprocess
import os
import zipfile
import json
from datetime import datetime

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

def main():
    # Create buildnumber.json
    print("Creating buildnumber.json...")
    version = "1.0.0"  # You may want to get this from a config file or as a parameter
    build_id = datetime.now().strftime("%Y%m%d%H%M%S")
    create_buildnumber_json(version, build_id)

    # Run setup.py build
    print("Running setup.py build...")
    run_command("python ..\\..\\app.py build")

    # Create a zip file with timestamp
    print("Creating zip file...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_dir = ".\\build\\exe.win-amd64-3.12"
    zip_filename = f".\\build\\portable\\mdu-portable_{timestamp}.zip"
    create_zip(source_dir, zip_filename)
    print(f"Created zip file: {zip_filename}")

    # Run Inno Setup
    print("Running Inno Setup...")
    inno_setup_path = r"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
    if not os.path.exists(inno_setup_path):
        print(f"Inno Setup not found at {inno_setup_path}")
        print("Please install Inno Setup or update the path in the script.")
        exit(1)
    run_command(f'"{inno_setup_path}" makeinstall.iss')

    print("Build process completed successfully!")

if __name__ == "__main__":
    main()
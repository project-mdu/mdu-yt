import argparse
import re
import os
import subprocess
from rich.console import Console
from rich.progress import Progress
from rich import print as rprint

def parse_arguments():
    parser = argparse.ArgumentParser(description="FFmpeg wrapper with progress bar")
    parser.add_argument("input_file", help="Input file path")
    return parser.parse_args()

def get_video_duration(input_file):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout)

def run_ffmpeg(input_file, output_file, duration, progress):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-c:v", "hevc_amf",
        "-c:a", "aac",
        "-b:v", "20M",
        "-preset", "ultrafast",
        "-strict", "experimental",
        output_file
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    task = progress.add_task("[cyan]Converting...", total=100)

    for line in process.stdout:
        matches = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
        if matches:
            hours, minutes, seconds = map(float, matches.groups())
            time_in_secs = hours * 3600 + minutes * 60 + seconds
            progress_percentage = min(100, time_in_secs / duration * 100)
            progress.update(task, completed=progress_percentage)

    process.wait()
    progress.update(task, completed=100)

def main():
    args = parse_arguments()
    input_file = args.input_file
    output_file = os.path.expanduser(f"{input_file}_converted.mp4")

    console = Console()

    try:
        duration = get_video_duration(input_file)
        
        with Progress() as progress:
            run_ffmpeg(input_file, output_file, duration, progress)
        
        rprint("[green]Conversion completed successfully![/green]")
    except Exception as e:
        rprint(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main()
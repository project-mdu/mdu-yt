import sys
import os
import subprocess
import re
import urllib.request
from yt_dlp import YoutubeDL
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.panel import Panel
from rich.text import Text

console = Console()

def sanitize_filename(title):
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace('\n', ' ').replace('\r', ' ')
    title = ' '.join(title.split())
    return title[:200]

def extract_video_audio_urls_and_title(youtube_url):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'quiet': True,
        'no_warnings': True,
        'youtube_include_dash_manifest': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            with console.status("[bold green]Extracting video information..."):
                info = ydl.extract_info(youtube_url, download=False)
            formats = info['formats']
            
            best_video = next((f for f in formats if f.get('height') == 1080 and f.get('acodec') == 'none'), None)
            if not best_video:
                best_video = next((f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none'), None)
            
            best_audio = next((f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none'), None)
            
            if not best_video or not best_audio:
                raise ValueError("Could not find suitable video and audio formats")
            
            title = info.get('title', 'Unknown Title')
            sanitized_title = sanitize_filename(title)
            
            return best_video['url'], best_audio['url'], sanitized_title, best_video.get('height', 'Unknown')
        
        except Exception as e:
            raise ValueError(f"An error occurred while extracting video info: {str(e)}")

def download_file(url, filename, progress: Progress, task: TaskID):
    def report_progress(blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        if totalsize > 0:
            percent = downloaded / totalsize
            progress.update(task, completed=int(percent * 100))

    urllib.request.urlretrieve(url, filename, reporthook=report_progress)

def merge_video_audio(video_file, audio_file, output_file):
    ffmpeg_path = 'ffmpeg.exe'  # Make sure ffmpeg.exe is in the same directory or provide the full path
    command = [ffmpeg_path, '-i', video_file, '-i', audio_file, '-c', 'copy', output_file]
    
    with console.status("[bold green]Merging video and audio..."):
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main(youtube_url):
    try:
        video_url, audio_url, video_title, video_height = extract_video_audio_urls_and_title(youtube_url)
        
        console.print(Panel(Text(f"Title: {video_title}\nResolution: {video_height}p", style="bold green")))

        video_file = f"{video_title}_video.mp4"
        audio_file = f"{video_title}_audio.m4a"
        output_file = f"{video_title}_merged.mp4"

        with Progress() as progress:
            video_task = progress.add_task("[red]Downloading video...", total=100)
            download_file(video_url, video_file, progress, video_task)

            audio_task = progress.add_task("[blue]Downloading audio...", total=100)
            download_file(audio_url, audio_file, progress, audio_task)

        merge_video_audio(video_file, audio_file, output_file)

        # Optionally, remove temporary files
        os.remove(video_file)
        os.remove(audio_file)

        console.print(f"[bold green]Process completed. Output file:[/bold green] {output_file}")

    except ValueError as e:
        console.print(f"[bold red]An error occurred:[/bold red] {str(e)}")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/bold red] python script.py <youtube_url>")
    else:
        youtube_url = sys.argv[1]
        main(youtube_url)
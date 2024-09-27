import subprocess
import os
import sys
import argparse

def get_video_info(url):
    """Get video title, video URL, and audio URL using yt-dlp."""
    command = [
        r"C:\Users\KinoBeddiez\Documents\MDU\bin\win\yt-dlp.exe",
        "-f", "bestvideo[height<=1080]+bestaudio[ext=m4a]",
        "-g",
        url
    ]

    # Get video title
    title_command = [
        r"C:\Users\KinoBeddiez\Documents\MDU\bin\win\yt-dlp.exe",
        "--get-title",
        url
    ]

    # Run the title command
    title = subprocess.run(title_command, capture_output=True, text=True)
    title_output = title.stdout.strip()

    # Run the video/audio command
    video_audio_urls = subprocess.run(command, capture_output=True, text=True)
    urls = video_audio_urls.stdout.strip().splitlines()

    if len(urls) < 2:
        print("Error: Could not retrieve both video and audio URLs.")
        sys.exit(1)

    video_url = urls[0]
    audio_url = urls[1]

    return title_output, video_url, audio_url

def download_with_aria2(video_url, audio_url, title):
    """Download video and audio using aria2c."""
    download_command = [
        "aria2c",
        "-x", "64",  # Number of connections
        "-s", "64",  # Number of splits
        "--dir", r"C:\Users\KinoBeddiez\Downloads",  # Download directory
        "-Z",
        "--out", f"videoplayback.webm",  # Output video filename
        video_url,
        "--out", f"audioplayback.m4a",  # Output audio filename
        audio_url
    ]

    subprocess.run(download_command)

def process_with_ffmpeg(title):
    """Combine video and audio using ffmpeg."""
    output_filename = f"{title}.mp4"
    video_filename = f"videoplayback.webm"
    audio_filename = f"audioplayback.m4a"

    ffmpeg_command = [
        "ffmpeg",
        "-i", video_filename,
        "-i", audio_filename,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_filename
    ]

    subprocess.run(ffmpeg_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Video Downloader using yt-dlp, aria2c, and ffmpeg.")
    parser.add_argument("url", help="The URL of the YouTube video to download.")
    args = parser.parse_args()

    # Step 1: Get video information
    title, video_url, audio_url = get_video_info(args.url)
    print(f"Title: {title}\nVideo URL: {video_url}\nAudio URL: {audio_url}")

    # Step 2: Download video and audio with aria2c
    download_with_aria2(video_url, audio_url, title)

    # Step 3: Process video and audio with ffmpeg
    process_with_ffmpeg(title)

    print("Download and processing complete!")

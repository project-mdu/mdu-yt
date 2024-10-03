import sys
import os
import subprocess
import re

# Add the directory containing yt_dlp to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(current_dir, '..', '..', 'src', 'core')
sys.path.append(yt_dlp_path)

from ytdlp.yt_dlp import YoutubeDL

def sanitize_filename(title):
    # Remove invalid filename characters and limit length
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace('\n', ' ').replace('\r', ' ')
    title = ' '.join(title.split())  # Remove extra spaces
    return title[:200]  # Limit filename length

def extract_video_audio_urls_and_title(youtube_url):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'quiet': True,
        'no_warnings': True,
        'youtube_include_dash_manifest': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            formats = info['formats']
            
            # Find best video stream (1080p or best available)
            best_video = next((f for f in formats if f.get('height') == 1080 and f.get('acodec') == 'none'), None)
            if not best_video:
                best_video = next((f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') == 'none'), None)
            
            # Find best audio stream
            best_audio = next((f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none'), None)
            
            if not best_video or not best_audio:
                raise ValueError("Could not find suitable video and audio formats")
            
            title = info.get('title', 'Unknown Title')
            sanitized_title = sanitize_filename(title)
            
            return best_video['url'], best_audio['url'], sanitized_title, best_video.get('height', 'Unknown')
        
        except Exception as e:
            raise ValueError(f"An error occurred while extracting video info: {str(e)}")

def download_and_convert_to_h264_qsv(video_url, audio_url, output_filename):
    ffmpeg_command = [
        'ffmpeg',
        '-i', video_url,
        '-i', audio_url,
        '-c:v', 'h264_qsv',  # Use QSV for H.264 encoding
        '-b:v', '25M',  # Set video bitrate to 25Mbps
        '-maxrate', '25M',  # Set max bitrate to 25Mbps
        '-bufsize', '50M',  # Set buffer size to 2x bitrate
        '-preset', 'medium',  # You can adjust the preset as needed
        '-c:a', 'aac',  # Use AAC for audio
        '-b:a', '320k',  # Set audio bitrate to 320kbps
        '-y',  # Overwrite output file if it exists
        output_filename
    ]
    
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Successfully downloaded and converted to {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during download and conversion: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
youtube_url = "https://www.youtube.com/watch?v=qXpZXsHJ4yA"  # Replace with desired video URL

try:
    video_url, audio_url, video_title, video_height = extract_video_audio_urls_and_title(youtube_url)
    print(f"Video URL: {video_url}")
    print(f"Audio URL: {audio_url}")
    print(f"Video Title: {video_title}")
    print(f"Video Resolution: {video_height}p")
    
    output_filename = f"{video_title}_{video_height}p_25Mbps.mp4"
    download_and_convert_to_h264_qsv(video_url, audio_url, output_filename)

except ValueError as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
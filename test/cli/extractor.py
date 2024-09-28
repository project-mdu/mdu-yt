import sys
import os

# Add the directory containing yt_dlp to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
yt_dlp_path = os.path.join(current_dir, '..', '..', 'src', 'core')
sys.path.append(yt_dlp_path)

from yt_dlp import YoutubeDL
from yt_dlp.extractor.youtube import YoutubeIE

def extract_video_audio_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio+bestvideo',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=False)
            
            formats = info.get('formats', [])
            best_video = next((f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none'), None)
            best_audio = next((f for f in formats if f['vcodec'] == 'none' and f['acodec'] != 'none'), None)
            
            if not best_video or not best_audio:
                raise ValueError("Could not find suitable video or audio formats")
            
            return best_video['url'], best_audio['url']
        
        except Exception as e:
            raise ValueError(f"An error occurred while extracting video info: {str(e)}")

def download_content(url, filename):
    ydl_opts = {
        'outtmpl': filename,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
youtube_url = "https://www.youtube.com/watch?v=qXpZXsHJ4yA"  # Replace with desired video URL

try:
    video_url, audio_url = extract_video_audio_url(youtube_url)
    
    print(f"Video URL: {video_url}")
    print(f"Audio URL: {audio_url}")
    
    # Uncomment these lines to actually download the content
    # download_content(video_url, "video.mp4")
    # download_content(audio_url, "audio.mp3")

except ValueError as e:
    print(f"An error occurred: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
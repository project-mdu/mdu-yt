import re
import urllib.request
import json
import urllib.error
import random
import time
import hashlib

INNERTUBE_CLIENT_IOS = {
    'INNERTUBE_CONTEXT': {
        'client': {
            'clientName': 'IOS',
            'clientVersion': '19.29.1',
            'deviceMake': 'Apple',
            'deviceModel': 'iPhone16,2',
            'userAgent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
            'osName': 'iPhone',
            'osVersion': '17.5.1.21F90',
        },
    },
    'INNERTUBE_CONTEXT_CLIENT_NAME': 5,
    'REQUIRE_JS_PLAYER': False,
}

def generate_ei_parameter():
    # This is a simplified version. A more accurate implementation would be needed.
    current_time = int(time.time())
    return hashlib.sha256(str(current_time).encode()).hexdigest()[:16]

def generate_api_headers():
    client_info = INNERTUBE_CLIENT_IOS
    timestamp = int(time.time())
    headers = {
        'X-YouTube-Client-Name': str(client_info['INNERTUBE_CONTEXT_CLIENT_NAME']),
        'X-YouTube-Client-Version': client_info['INNERTUBE_CONTEXT']['client']['clientVersion'],
        'User-Agent': client_info['INNERTUBE_CONTEXT']['client']['userAgent'],
        'X-YouTube-Time-Zone': 'UTC',
        'X-YouTube-Utc-Offset': '0',
        'X-YouTube-Ad-Signals': f'dt={timestamp}&flash=0&frm&u_tz=0&u_his=6&u_java&u_h=1080&u_w=1920&u_ah=1080&u_aw=1920&u_cd=24&u_nplug=0&u_nmime=0',
    }
    return headers

def select_best_format(formats):
    video_formats = [f for f in formats if f.get('mimeType', '').startswith('video')]
    audio_formats = [f for f in formats if f.get('mimeType', '').startswith('audio')]
    
    best_video = max(video_formats, key=lambda x: int(x.get('bitrate', 0)), default=None)
    best_audio = max(audio_formats, key=lambda x: int(x.get('bitrate', 0)), default=None)
    
    return best_video, best_audio

def extract_video_id(url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def build_url_with_params(base_url, params):
    return f"{base_url}{'&' if '?' in base_url else '?'}{urllib.parse.urlencode(params)}"

def extract_video_audio_url(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Could not extract video ID from the URL")

    headers = generate_api_headers()
    ei = generate_ei_parameter()
    
    player_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        req = urllib.request.Request(player_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
    except urllib.error.HTTPError as e:
        raise ValueError(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"Failed to reach the server. Reason: {e.reason}")
    
    video_info_match = re.search(r"ytInitialPlayerResponse\s*=\s*({.+?})\s*;", html)
    if not video_info_match:
        raise ValueError("Could not find ytInitialPlayerResponse in the page")
    
    video_info = json.loads(video_info_match.group(1))
    
    formats = video_info.get('streamingData', {}).get('formats', [])
    adaptive_formats = video_info.get('streamingData', {}).get('adaptiveFormats', [])
    
    all_formats = formats + adaptive_formats
    
    best_video, best_audio = select_best_format(all_formats)
    
    if not best_video or not best_audio:
        raise ValueError("Could not find suitable video or audio formats")
    
    common_params = {
        'ei': ei,
        'rqh': '1',
        'gir': 'yes',
    }
    
    video_params = common_params.copy()
    video_params.update({
        'itag': best_video['itag'],
        'clen': best_video.get('contentLength', ''),
    })
    
    audio_params = common_params.copy()
    audio_params.update({
        'itag': best_audio['itag'],
        'clen': best_audio.get('contentLength', ''),
    })
    
    video_url = build_url_with_params(best_video['url'], video_params)
    audio_url = build_url_with_params(best_audio['url'], audio_params)
    
    return video_url, audio_url

def download_content(url, filename):
    urllib.request.urlretrieve(url, filename)

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
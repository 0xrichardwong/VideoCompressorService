import sys
# passの設定 (pip showで出てきた、LocationのPASSを以下に設定)
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages')

# passの設定はimportするモジュールより前に設定
import ffmpeg
import json

def convert_to_mp3(video_file, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.mp3'):
    """
    Converts an MP4 video file to an MP3 audio file.
    
    Args:
    - video_file (str): Path to the input video file.
    - output_file (str): Path to the output audio file (default: 'output.mp3').
    
    Raises:
    - ffmpeg.Error: If an error occurs during the conversion process.
    """
    try:
        # Load the input video file
        stream = ffmpeg.input(video_file)
        
        # Set the output file path and format
        stream = ffmpeg.output(stream, output_file)
        
        # Run the ffmpeg command to process the conversion
        ffmpeg.run(stream)
        
    except ffmpeg.Error as e:
        # Handle ffmpeg errors by printing the error message
        print(f"An error occurred: {e.stderr.decode()}")
        
        # Re-raise the exception to notify the caller about the failure
        raise

def compressSize(input_file, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.mp4', bitrate='0.5M'):
    """
    Compresses the video size by reducing the bitrate.
    Args:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output compressed video file.
    - bitrate (str): Target bitrate for the compressed video (default: '0.5M').
    """
    ffmpeg.input(input_file).output(output_file, video_bitrate=bitrate).run()

def changeResolution(input_file, w, h, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.mp4'):
    """
    Changes the resolution of the video.
    Args:
    - input_file (str): Path to the input video file.
    - width (int): Target width of the video.
    - height (int): Target height of the video.
    - output_file (str): Path to the output video file with the new resolution (default: 'newResolution.mp4').
    """
    ffmpeg.input(input_file).output(output_file, vf=f'scale={w}:{h}').run()

def changeAspectRatio(input_file, aspect_ratio, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.mp4'):
    """
    Changes the aspect ratio of the video.
    Args:
    - input_file (str): Path to the input video file.
    - aspect_ratio (str): Target aspect ratio (e.g., '16:9', '4:3').
    - output_file (str): Path to the output video file with the new aspect ratio (default: 'newAspectRatio.mp4').
    """
    ffmpeg.input(input_file).output(output_file, aspect=aspect_ratio).run()

def convert_to_GIF(input_file, start_time, duration, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.gif', format='gif'):
    """
    Converts a segment of the video to GIF or WEBM format.
    Args:
    - input_file (str): Path to the input video file.
    - start_time (str): Start time of the segment (e.g., '00:00:10' for 10 seconds).
    - duration (str): Duration of the segment (e.g., '5' for 5 seconds).
    - output_file (str): Path to the output GIF or WEBM file (default: 'output.gif').
    - format (str): Target format ('gif' or 'webm', default: 'gif').
    """
    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, format=format).run()

def change_speed(input_file, speed_factor, output_file='/Users/richardwong_/Documents/Web3/Recursionist/2.Backend2/videoCompressor/temp/output.mp4'):
    """
    Changes the speed of the video.
    Args:
    - input_file (str): Path to the input video file.
    - speed_factor (float): Speed factor (e.g., 0.5 for half speed, 2.0 for double speed).
    - output_file (str): Path to the output video file with the changed speed (default: 'newSpeed.mp4').
    """
    # Ensure speed_factor is a float
    speed_factor = float(speed_factor)
    # Adjust the video speed
    ffmpeg.input(input_file).filter('setpts', f'{1/speed_factor}*PTS').output(output_file).run()

# Example usage:
# convert_to_mp3('cat.mp4')
# compressSize('cat.mp4')
# changeResolution('cat.mp4', 1280, 720)
# changeAspectRatio('cat.mp4', '16:9')
# convert_to_GIF('cat.mp4', '00:00:10', '5')
# change_speed('cat.mp4', 2.0)

"""
json_message = json.dumps({
    "method": "convert_to_mp3",
    "params": ['cat.mp4']
})

# Parse the JSON message to a Python dictionary
message = json.loads(json_message)

edit_method = message['method']
edit_method = globals()[edit_method]
edit_params = message['params']

edit_method(*edit_params)
"""
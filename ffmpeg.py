import ffmpeg

input = 'cat.mp4'

def mp4_to_mp3(video_file, output_file='output.mp3'):
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

def compressSize(input_file, output_file, bitrate='1M'):
    """
    Compresses the video size by reducing the bitrate.
    Args:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output compressed video file.
    - bitrate (str): Target bitrate for the compressed video (default: '1M').
    """
    ffmpeg.input(input_file).output(output_file, video_bitrate=bitrate).run()

def changeResolution(input_file, output_file, width, height):
    """
    Changes the resolution of the video.
    Args:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output video file with the new resolution.
    - width (int): Target width of the video.
    - height (int): Target height of the video.
    """
    ffmpeg.input(input_file).output(output_file, vf=f'scale={width}:{height}').run()

def changeAspectRatio(input_file, output_file, aspect_ratio):
    """
    Changes the aspect ratio of the video.
    Args:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output video file with the new aspect ratio.
    - aspect_ratio (str): Target aspect ratio (e.g., '16:9', '4:3').
    """
    ffmpeg.input(input_file).output(output_file, aspect=aspect_ratio).run()

def convert_to_GIF_or_WEBM(input_file, output_file, start_time, duration, format='gif'):
    """
    Converts a segment of the video to GIF or WEBM format.
    Args:
    - input_file (str): Path to the input video file.
    - output_file (str): Path to the output GIF or WEBM file.
    - start_time (str): Start time of the segment (e.g., '00:00:10' for 10 seconds).
    - duration (str): Duration of the segment (e.g., '5' for 5 seconds).
    - format (str): Target format ('gif' or 'webm', default: 'gif').
    """
    ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file, format=format).run()




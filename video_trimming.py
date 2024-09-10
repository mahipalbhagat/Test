from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def to_seconds(time_str):
    time_components = [int(i) for i in time_str.split(':')]
    if len(time_components) == 2:  # MM:SS format
        return (time_components[0] * 60) + time_components[1]
    elif len(time_components) == 3:  # HH:MM:SS format
        return (time_components[0] * 3600) + (time_components[1] * 60) + time_components[2]
    else:
        raise ValueError("Invalid time format. Please provide either MM:SS or HH:MM:SS.")

def trim_media_moviepy(input_file, output_file, start_time, end_time):
    try:
        start_seconds = to_seconds(start_time)
        end_seconds = to_seconds(end_time)

        with VideoFileClip(input_file) as video:
            trimmed_video = video.subclip(start_seconds, end_seconds)
            trimmed_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

        print(f"Media trimmed successfully from {start_time} to {end_time}.")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = input("Enter the input video file path: ")
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_trimmed{ext}"
    start_time = input("Enter the start time in format MM:SS or HH:MM:SS: ")
    end_time = input("Enter the end time in format MM:SS or HH:MM:SS: ")
    trim_media_moviepy(input_file, output_file, start_time, end_time)

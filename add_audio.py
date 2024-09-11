import moviepy.editor as mp
import os
 
def add_audio_to_video(video_path, audio_path, output_path, start_time, end_time):
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Convert start_time and end_time to seconds
        start_seconds = convert_to_seconds(start_time)
        end_seconds = convert_to_seconds(end_time)
        # Load and trim the video
        video = mp.VideoFileClip(video_path).subclip(start_seconds, end_seconds)
        # Load and trim the audio
        audio = mp.AudioFileClip(audio_path).subclip(start_seconds, end_seconds)
        # Set the audio of the video clip
        video = video.set_audio(audio)
        # Write the result to a file
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        # Close the video and audio to free up resources
        video.close()
        audio.close()
        print(f"Video saved successfully to {output_path}")
 
    except Exception as e:
        print(f"An error occurred: {e}")
 
def convert_to_seconds(time_str):
    try:
        hours, minutes, seconds = map(float, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Please use HH:MM:SS format.")
 
if __name__ == "__main__":
    # Get input file paths and parameters from the user
    video_path = input("Enter the path of the video file (without audio): ").strip()
    audio_path = input("Enter the path of the audio file to be added: ").strip()
    output_path = input("Enter the output path for the video with added audio (including file extension, e.g., 'output_video.mp4'): ").strip()
    start_time = input("Enter the start time to trim the video and audio (in HH:MM:SS format, e.g., 00:00:05): ").strip()
    end_time = input("Enter the end time to trim the video and audio (in HH:MM:SS format, e.g., 00:00:20): ").strip()
    # Add audio to the trimmed video
    add_audio_to_video(video_path, audio_path, output_path, start_time, end_time)
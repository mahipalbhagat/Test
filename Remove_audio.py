from moviepy.editor import VideoFileClip
import os

def remove_audio_moviepy(input_file, output_file):
    try:
        with VideoFileClip(input_file) as video:
            video_no_audio = video.without_audio()
            video_no_audio.write_videofile(output_file, codec='libx264')
 
        print(f"Audio removed successfully from {input_file}.")
        return True
 
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = input("Enter the input video file path: ")
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_no_audio{ext}"
    remove_audio_moviepy(input_file, output_file)
ahbhbshbhbabbadshdb
from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path):
    audio_path = os.path.splitext(video_path)[0] + '.mp3'
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    video.close()
    audio.close()
    return audio_path

if __name__ == "__main__":
    video_path = input("Enter the path of the video file: ")
    audio_path = extract_audio(video_path)
    print(f"Audio extracted and saved to {audio_path}")

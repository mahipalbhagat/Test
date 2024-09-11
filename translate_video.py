import moviepy.editor as mp
import openai
from gtts import gTTS
import os
import subprocess
from pydub import AudioSegment
from pydub.effects import normalize

openai.api_key = "my api key"

languages = {
    'German': 'de',
    'French': 'fr',
    'Spanish': 'es',
    'Italian': 'it',
    'Dutch': 'nl',
    'Norwegian': 'no',
    'Portuguese': 'pt',
    'Finnish': 'fi',
    'Swedish': 'sv',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Thai': 'th',
    'Traditional Chinese': 'zh-TW',
    'Hindi': 'hi',
    'English': 'en'
}

def run_ffmpeg_command(command):
    subprocess.run(command, check=True)

def extract_audio(video_file):
    video = mp.VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file)
    return audio_file, video.duration

def preprocess_audio(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    normalized_audio = normalize(audio)
    processed_audio_path = "processed_" + audio_file_path
    normalized_audio.export(processed_audio_path, format="wav")
    return processed_audio_path

def audio_to_text_with_whisper(audio_file):
    with open(audio_file, "rb") as f:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=f,
            language="en"
        )
    print("Whisper response:", response)
    return response['text']

def translate_text_openai(text, target_lang):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that translates English to {target_lang}."},
                {"role": "user", "content": text}
            ],
            max_tokens=1000
        )
        translation = response.choices[0].message['content'].strip()
        return translation
    except Exception as e:
        print(f"Error translating text to {target_lang}: {e}")
        return text

def create_audio_for_segment(translated_text, lang_code, segment_index):
    tts = gTTS(text=translated_text, lang=lang_code)
    tts_file = f"temp_{lang_code}_{segment_index}.mp3"
    tts.save(tts_file)
    audio = AudioSegment.from_file(tts_file)
    os.remove(tts_file)
    adjusted_audio_file = f"adjusted_{lang_code}_{segment_index}.wav"
    audio.export(adjusted_audio_file, format="wav")
    print(f"Created adjusted audio file: {adjusted_audio_file}")
    return adjusted_audio_file

def combine_audio_segments(audio_segments):
    combined_audio = AudioSegment.silent(duration=0)
    for segment in audio_segments:
        audio_segment = AudioSegment.from_file(segment)
        combined_audio += audio_segment
        os.remove(segment)
    combined_audio_file = "combined_translated_audio.wav"
    combined_audio.export(combined_audio_file, format="wav")
    print(f"Combined audio file created: {combined_audio_file}")
    return combined_audio_file

def combine_audio_with_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy',
        '-map', '0:v:0', '-map', '1:a:0', output_file, '-y'
    ]
    run_ffmpeg_command(command)

def translate_video(video_file, selected_languages):
    audio_file, video_duration = extract_audio(video_file)
    transcription_text = audio_to_text_with_whisper(audio_file)

    if not transcription_text:
        print("Error: Transcription text not found")
        return

    words = transcription_text.split()
    num_segments = 10
    words_per_segment = len(words) // num_segments
    segments = [" ".join(words[i*words_per_segment:(i+1)*words_per_segment]) for i in range(num_segments)]
    segment_durations = [(video_duration / num_segments) * 1000 for _ in range(num_segments)]

    for lang_name in selected_languages:
        lang_code = languages.get(lang_name.strip())
        if not lang_code:
            print(f"Error: Language '{lang_name}' is not supported.")
            continue

        audio_segments = []

        for i, segment in enumerate(segments):
            translated_text = translate_text_openai(segment, target_lang=lang_name)
            adjusted_audio_file = create_audio_for_segment(translated_text, lang_code, i)
            audio_segments.append(adjusted_audio_file)

        combined_audio_file = combine_audio_segments(audio_segments)

        output_file = f"{video_file.rsplit('.', 1)[0]}_{lang_code}.mp4"
        combine_audio_with_video(video_file, combined_audio_file, output_file)

        os.remove(combined_audio_file)
        print(f"Processed, merged, and generated translation for {lang_name}.")

if __name__ == "__main__":
    video_file = input("Enter the video file path: ")
    selected_languages = input("Enter full language names separated by commas (e.g., 'German, French, Spanish'): ").split(',')
    translate_video(video_file, selected_languages)

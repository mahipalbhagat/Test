import openai
import pyttsx3
from gtts import gTTS
import os
import pygame
import uuid

openai.api_key = "my api key"

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

def text_to_speech_pyttsx3(text, voice_id=None):
    engine = pyttsx3.init()
    if voice_id is not None:
        engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

def text_to_speech_gtts(text, lang='en', save_path=None):
    if save_path is None:
        save_path = f"output_{uuid.uuid4().hex}.mp3"
    try:
        print(f"Saving TTS output to {save_path}...")
        tts = gTTS(text=text, lang=lang)
        tts.save(save_path)
        print(f"File saved successfully at {save_path}.")
        pygame.mixer.init()
        pygame.mixer.music.load(save_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        pygame.mixer.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name} - {voice.id}")
    google_voices = [
        "US English",
        "French Accent",
        "Spanish Accent",
        "German Accent",
        "Italian Accent",
        "Japanese Accent",
        "Indian English Accent",
        "African English Accent",
        "Russian Accent",
        "Chinese Accent - Mandarin",
        "Korean Accent",
        "Arabic Accent"
    ]
    for i, voice_name in enumerate(google_voices, start=len(voices)):
        print(f"{i}: {voice_name} - gtts")
    return voices

def main():
    voices = list_voices()
    choice = input("Enter the number of the voice you want to use (default is the first voice): ")
    try:
        selected_voice = int(choice)
        gtts_lang = None
        if selected_voice < len(voices):
            selected_voice_id = voices[selected_voice].id
            use_gtts = False
        elif selected_voice == len(voices):
            use_gtts = True
            gtts_lang = 'en'
        elif selected_voice == len(voices) + 1:
            use_gtts = True
            gtts_lang = 'fr'
        elif selected_voice == len(voices) + 2:
            use_gtts = True
            gtts_lang = 'es'
        elif selected_voice == len(voices) + 3:
            use_gtts = True
            gtts_lang = 'de'
        elif selected_voice == len(voices) + 4:
            use_gtts = True
            gtts_lang = 'it'
        elif selected_voice == len(voices) + 5:
            use_gtts = True
            gtts_lang = 'ja'
        elif selected_voice == len(voices) + 6:
            use_gtts = True
            gtts_lang = 'en-in'
        elif selected_voice == len(voices) + 7:
            use_gtts = True
            gtts_lang = 'en-ng'
        elif selected_voice == len(voices) + 8:
            use_gtts = True
            gtts_lang = 'ru'
        elif selected_voice == len(voices) + 9:
            use_gtts = True
            gtts_lang = 'zh-cn'
        elif selected_voice == len(voices) + 10:
            use_gtts = True
            gtts_lang = 'ko'
        elif selected_voice == len(voices) + 11:
            use_gtts = True
            gtts_lang = 'ar'
        else:
            raise ValueError("Invalid choice.")
    except (ValueError, IndexError):
        print("Invalid choice. Using default voice.")
        selected_voice_id = voices[0].id if voices else None
        use_gtts = False

    user_input = input("Enter the text you want to convert to speech: ")
    if use_gtts:
        save_path = input("Enter a file name to save the audio (e.g., 'output.mp3'), or press Enter to use a unique name: ").strip()
        save_path = save_path if save_path else None
        text_to_speech_gtts(user_input, lang=gtts_lang, save_path=save_path)
    else:
        text_to_speech_pyttsx3(user_input, voice_id=selected_voice_id)

if __name__ == "__main__":
    main()

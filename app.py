from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import time

app = Flask(__name__)

output_langs = ["hi", "kn", "mr", "ta", "bn", "te", "gu"]  # Hindi, Kannada, Marathi, Tamil, Bengali, Telugu, Gujarati

# Initialize pygame mixer
pygame.mixer.init()

translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    speech_text = request.json.get('speech_text')
    print(f"Received speech text: {speech_text}")
    translations = {}
    for lang in output_langs:
        try:
            translated_text = translator.translate(speech_text, dest=lang).text
            translations[lang] = translated_text
            print(f"Translated Text in {lang}: {translated_text}")

            filename = f'voice_{lang}_{int(time.time())}.mp3'
            tts = gTTS(translated_text, lang=lang)
            tts.save(filename)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"An error occurred with language {lang}: {e}")

    return jsonify(translations)

if __name__ == '__main__':
    app.run(debug=True)

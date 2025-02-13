import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import time

# Define multiple output languages
output_langs = ["hi", "kn", "mr", "ta", "bn", "te", "gu"]  # Hindi, Kannada, Marathi, Tamil, Bengali, Telugu, Gujarati

# Initialize pygame mixer
pygame.mixer.init()

r = sr.Recognizer()
translator = Translator()

while True:
    with sr.Microphone() as source:
        print("Speak Now!")
        audio = r.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            speech_text = r.recognize_google(audio)
            print("Recognized Speech:", speech_text)
            
            for lang in output_langs:
                try:
                    # Translate the recognized text to the target language
                    translated_text = translator.translate(speech_text, dest=lang).text
                    print(f"Translated Text in {lang}:", translated_text)
                    
                    # Convert the translated text to speech
                    filename = f'voice_{lang}_{int(time.time())}.mp3'  # Use a unique filename based on timestamp
                    tts = gTTS(translated_text, lang=lang)
                    tts.save(filename)
                    
                    # Play the generated speech using pygame
                    pygame.mixer.music.load(filename)
                    pygame.mixer.music.play()

                    # Wait until the audio finishes playing
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)  # Add a small delay to avoid busy-waiting
                    
                    # Ensure the file is fully released before trying to delete it
                    pygame.mixer.music.unload()
                    
                    # Remove the temporary audio file
                    if os.path.exists(filename):
                        os.remove(filename)
                except Exception as e:
                    print(f"An error occurred with language {lang}: {e}")
                
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Ask the user if they want to continue or break the loop
    continue_prompt = input("Do you want to continue listening? (yes/no): ")
    if continue_prompt.strip().lower() != 'yes':
        break

# Quit pygame mixer
pygame.mixer.quit()

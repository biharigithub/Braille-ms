import pyttsx3
import uuid
import os

def text_to_speech(text, language='english'):
    try:
        # Use a temporary unique filename
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("static/audio", filename)

        # Initialize pyttsx3 engine
        engine = pyttsx3.init()

        # Set language voice (adjust based on system availability)
        voices = engine.getProperty('voices')
        for voice in voices:
            if language == 'hindi' and 'hi' in voice.languages[0].decode():
                engine.setProperty('voice', voice.id)
                break
            elif language == 'english' and ('en' in voice.languages[0].decode() or 'en' in voice.name.lower()):
                engine.setProperty('voice', voice.id)
                break

        # Save audio to file
        engine.save_to_file(text, filepath)
        engine.runAndWait()

        return f"/static/audio/{filename}"
    except Exception as e:
        raise Exception(f"pyttsx3 TTS failed: {str(e)}")

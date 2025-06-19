# utils/speech_processor.py (New)
import pyttsx3
import tempfile
import base64
import os

def text_to_speech(text, language='english'):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Set voice for Hindi or English
        for voice in voices:
            if language == 'hindi' and ('hi' in voice.id or 'Hindi' in voice.name):
                engine.setProperty('voice', voice.id)
                break
            elif language == 'english' and ('en' in voice.id or 'English' in voice.name):
                engine.setProperty('voice', voice.id)
                break

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            filename = tmp.name
        engine.save_to_file(text, filename)
        engine.runAndWait()

        with open(filename, 'rb') as f:
            audio_data = base64.b64encode(f.read()).decode('utf-8')

        os.remove(filename)
        return audio_data
    except Exception as e:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise e

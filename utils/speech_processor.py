import pyttsx3
import tempfile
import base64
import os

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # You can adjust speed
        engine.setProperty('volume', 1.0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            filename = f.name
        engine.save_to_file(text, filename)
        engine.runAndWait()

        # Read audio as base64
        with open(filename, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

        os.remove(filename)
        return audio_data

    except Exception as e:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise e

from gtts import gTTS
import tempfile
import base64
import os

def text_to_speech(text, language='english'):
    try:
        lang_code = 'en' if language.lower() == 'english' else 'hi'

        if not text.strip():
            raise ValueError("Empty text cannot be converted.")

        # Generate speech
        tts = gTTS(text=text, lang=lang_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            filename = tmp.name
            tts.save(filename)

        with open(filename, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

        return audio_data

    except Exception as e:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise e

    finally:
        # Ensure file is deleted even after success
        try:
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
        except:
            pass

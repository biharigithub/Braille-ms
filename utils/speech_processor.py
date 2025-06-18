from gtts import gTTS
import tempfile
import base64
import os

def text_to_speech(text, language='english'):
    try:
        lang_code = 'en' if language.lower() == 'english' else 'hi'

        # Generate speech using gTTS
        tts = gTTS(text=text, lang=lang_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            filename = tmp.name
            tts.save(filename)

        with open(filename, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

        os.remove(filename)
        return audio_data

    except Exception as e:
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        raise e

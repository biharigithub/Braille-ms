# ✅ Fixed: speech_processor.py using gTTS, works in Android WebView
from gtts import gTTS
import tempfile
import base64
import os

def text_to_speech(text, language='english'):
    try:
        lang_code = 'en' if language.lower() == 'english' else 'hi'

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

# ✅ app.py (relevant /api/text-to-speech endpoint)
@app.route('/api/text-to-speech', methods=['POST'])
def convert_text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'english')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        audio_data = text_to_speech(text, language)
        return jsonify({'audio_data': audio_data})
    except Exception as e:
        logging.error(f"Error converting text to speech: {str(e)}")
        return jsonify({'error': f'Error converting text to speech: {str(e)}'}), 500

# ✅ JS (relevant part in image_to_braille.js)
readAloudButton.addEventListener('click', function () {
    const text = extractedTextElement.textContent;
    const language = languageSelect.value || 'english';
    if (!text || text.trim() === '') {
        showNotification('Error', 'No text to read');
        return;
    }
    readAloud(text, language);
});

function readAloud(text, language) {
    fetch('/api/text-to-speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text, language: language }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error', data.error);
                return;
            }
            const audio = new Audio('data:audio/mp3;base64,' + data.audio_data);
            audio.play().catch(err => console.error('Playback error:', err));
        })
        .catch(error => {
            console.error('Read Aloud Error:', error);
            showNotification('Error', 'Failed to read text aloud');
        });
}

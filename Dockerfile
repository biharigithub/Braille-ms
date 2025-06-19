FROM python:3.10-slim

# ✅ Install dependencies (Tesseract + espeak + audio support)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    espeak-ng \
    ffmpeg \  # ✅ Add ffmpeg for audio encoding (required by pyttsx3 sometimes)
    libsm6 libxext6 libxrender-dev \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]

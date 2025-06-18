FROM python:3.10-slim

# Install tesseract with Hindi + English, espeak for future-proof TTS
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    espeak-ng \
    libsm6 libxext6 libxrender-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

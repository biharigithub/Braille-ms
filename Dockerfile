# Base image with Python 3.10
FROM python:3.10-slim

# Install system dependencies for tesseract & OpenCV
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev \
                       tesseract-ocr-eng tesseract-ocr-hin \
                       libglib2.0-0 libsm6 libxext6 libxrender-dev \
                       gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy code and install dependencies
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for gunicorn
EXPOSE 5000

# Start Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

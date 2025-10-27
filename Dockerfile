FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including espeak-ng
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download TTS model
RUN python -c "from TTS.api import TTS; TTS(model_name='tts_models/en/vctk/vits', progress_bar=False, gpu=False)"

# Copy app code
COPY . .

# Expose port
EXPOSE 5002

# Run with Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5002", "app:app"]

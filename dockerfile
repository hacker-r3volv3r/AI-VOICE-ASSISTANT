FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgomp1 \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip \
    && unzip vosk-model-small-ru-0.22.zip \
    && mv vosk-model-small-ru-0.22 model \
    && rm vosk-model-small-ru-0.22.zip

COPY . .

CMD ["python", "bot.py"]

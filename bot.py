import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from vosk import Model, KaldiRecognizer
import json
from pydub import AudioSegment

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)

# Инициализация БД
conn = sqlite3.connect('/app/data/assistant.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    start_time DATETIME,
    end_time DATETIME,
    description TEXT
)
""")
conn.commit()

# Vosk модель
model = Model("/app/model")
recognizer = KaldiRecognizer(model, 16000)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🚀 Привет! Я твой голосовой ассистент. Отправь мне голосовое сообщение!")

@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_voice(message: types.Message):
    try:
        voice = await message.voice.get_file()
        await voice.download("temp.ogg")
        
        audio = AudioSegment.from_ogg("temp.ogg")
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export("temp.wav", format="wav")
        
        with open("temp.wav", "rb") as f:
            if recognizer.AcceptWaveform(f.read()):
                text = json.loads(recognizer.Result())["text"]
                await message.reply(f"🎤 Вы сказали: {text}")
        
        os.remove("temp.ogg")
        os.remove("temp.wav")
        
    except Exception as e:
        await message.reply(f"❌ Ошибка: {str(e)}")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
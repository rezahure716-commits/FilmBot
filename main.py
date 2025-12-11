import telebot
import time
import os
from flask import Flask
from threading import Thread

# --- بخش 1: سرور ساختگی برای بیدار نگه داشتن Render ---
app = Flask('')

@app.route('/')
def home():
    return "Robot is Alive!"

def run_http():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http)
    t.start()
# -----------------------------------------------------

# --- بخش 2: کد اصلی ربات ---
# توکن شما
BOT_TOKEN = '8436713301:AAFuS5ilCZuvG7C2D9xxsNyHvCaJGkPU0w' 
bot = telebot.TeleBot(BOT_TOKEN)

# آیدی فایل فیلم (تست)
FILE_ID_MOVIE = 'BAACAgQAAxkBAAICaW_I6wNn2Yg-XwABoQ1gP30wF1k-AAI3AQACsFzYUZI51d02oAAAAg' 

@bot.message_handler(commands=['start'])
def send_movie(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "⏳ فیلم در حال ارسال است...")

    try:
        # ارسال فیلم
        sent_video = bot.send_video(
            chat_id, 
            FILE_ID_MOVIE, 
            caption="⚠️ این فیلم تا ۳۰ ثانیه دیگر پاک می‌شود."
        )
        # حذف پیام "در حال ارسال"
        bot.delete_message(chat_id, msg.message_id)

        # صبر کردن ۳۰ ثانیه
        time.sleep(30)

        # حذف فیلم
        bot.delete_message(chat_id, sent_video.message_id)
        bot.send_message(chat_id, "✅ فیلم طبق زمان‌بندی حذف شد.")

    except Exception as e:
        bot.send_message(chat_id, "❌ خطا در ارسال یا حذف.")
        print(e)

# --- بخش 3: اجرا ---
keep_alive() 
bot.polling(non_stop=True)

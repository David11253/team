from telegram import Bot
from telegram.ext import CommandHandler, Updater
import os
from flask import Flask, request

TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Твой токен
bot = Bot(TOKEN)

app = Flask(__name__)

# Команда /start для бота
def start(update, context):
    update.message.reply_text("Привет, я твой бот!")

# Инициализация Updater и Dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Добавление обработчика команды
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Flask-сервер
@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    updater.start_polling()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

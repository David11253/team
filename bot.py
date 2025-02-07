from telegram import Bot
from telegram.ext import CommandHandler, Application
import os
from flask import Flask

TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Твой токен

app = Flask(__name__)

# Команда /start для бота
async def start(update, context):
    await update.message.reply_text("Привет, я твой бот!")

# Создаем приложение
application = Application.builder().token(TOKEN).build()

# Добавление обработчика команды
start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

# Flask-сервер
@app.route('/')
def index():
    return "Hello, world!"

if __name__ == '__main__':
    application.run_polling()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

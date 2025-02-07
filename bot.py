import os
import telebot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, render_template, request
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен для бота и ID группы
TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Твой токен
bot = telebot.TeleBot(TOKEN)

# ID твоей группы в Telegram
GROUP_ID = '-1002428849357'  # ID твоей группы

# Создаем Flask приложение
app = Flask(__name__)

# Функция для отправки заявки в группу
def send_application_to_group(data):
    # Формируем сообщение с заявкой
    message = f"Новая заявка на вступление:\n"
    message += f"Никнейм: {data['nickname']}\n"
    message += f"ПК или Мб: {data['device']}\n"
    message += f"Сервер: {data['server']}\n"
    message += f"Редстоун (1-10): {data['redstone']}\n"
    message += f"ПвП или ПвЕ: {data['pvp_pve']}\n"
    message += f"Часов в день: {data['playtime']}\n"
    message += f"Учеба: {data['study']}\n"
    message += f"Тимейты: {data['teammates']}\n"
    message += f"Страна: {data['country']}\n"
    message += f"Возраст: {data['age']}\n"
    message += f"Интернет: {data['internet']}\n"
    message += f"Телега/Телефон: {data['contact']}\n"

    # Добавляем кнопки для голосования
    keyboard = [
        [InlineKeyboardButton("Принять", callback_data='accept')],
        [InlineKeyboardButton("Отклонить", callback_data='reject')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение в группу
    bot.send_message(chat_id=GROUP_ID, text=message, reply_markup=reply_markup)

# Flask маршруты для сайта
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = {
        'nickname': request.form['nickname'],
        'device': request.form['device'],
        'server': request.form['server'],
        'redstone': request.form['redstone'],
        'pvp_pve': request.form['pvp_pve'],
        'playtime': request.form['playtime'],
        'study': request.form['study'],
        'teammates': request.form['teammates'],
        'country': request.form['country'],
        'age': request.form['age'],
        'internet': request.form['internet'],
        'contact': request.form['contact']
    }

    # Отправляем заявку в группу
    send_application_to_group(data)

    return "Заявка отправлена и ожидает голосования."

if __name__ == '__main__':
    # Запуск Flask-приложения
    port = int(os.environ.get("PORT", 5000))  # Используем переменную окружения PORT для Render
    app.run(host='0.0.0.0', port=port)

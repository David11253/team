import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from flask import Flask, render_template, request
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен для бота и ID группы
TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Замените на ваш токен
GROUP_ID = '-1002428849357'  # ID или username вашей группы

# Создаем Flask приложение
app = Flask(__name__)

# Создаем приложение для Telegram бота
application = Application.builder().token(TOKEN).build()

# Функция для обработки команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я бот для подачи заявки. Заполни форму на сайте.")

# Функция для отправки заявки в группу
async def send_application_to_group(update: Update, context: CallbackContext, data: dict):
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
    await application.bot.send_message(chat_id=GROUP_ID, text=message, reply_markup=reply_markup)

# Обработчик нажатий на кнопки (голосование)
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Получаем выбранную кнопку
    action = query.data

    if action == 'accept':
        response = "Заявка принята!"
    elif action == 'reject':
        response = "Заявка отклонена!"
    
    # Отправляем сообщение с результатом голосования
    await query.edit_message_text(text=f"Голосование завершено. {response}")

# Добавляем обработчики команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

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
    application.loop.create_task(send_application_to_group(None, None, data))

    return "Заявка отправлена и ожидает голосования."

if __name__ == '__main__':
    # Запуск бота в отдельном потоке
    application.run_polling()

    # Запуск Flask-приложения на правильном порту
    port = int(os.environ.get("PORT", 5000))  # Используем переменную окружения PORT для Render
    app.run(host='0.0.0.0', port=port)

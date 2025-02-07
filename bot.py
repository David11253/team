import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request

API_TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Твой токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Flask-сервер для обработки данных формы
app = Flask(__name__)

# ID твоей группы в Telegram
GROUP_ID = '-1002428849357'

# Логирование
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь свою заявку через форму на сайте.")

@app.route('/submit', methods=['POST'])
def submit_form():
    # Получаем данные из формы
    nickname = request.form.get('nickname')
    device = request.form.get('device')
    server = request.form.get('server')
    redstone = request.form.get('redstone')
    pvp_pve = request.form.get('pvp_pve')
    playtime = request.form.get('playtime')
    study = request.form.get('study')
    teammates = request.form.get('teammates')
    country = request.form.get('country')
    age = request.form.get('age')
    internet = request.form.get('internet')
    contact = request.form.get('contact')

    # Создаем кнопку для голосования
    keyboard = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton("Принять", callback_data="accept")
    button_no = InlineKeyboardButton("Отклонить", callback_data="reject")
    keyboard.add(button_yes, button_no)

    # Отправляем заявку в группу с голосованием
    bot.send_message(GROUP_ID, f"Новая заявка на вступление:\n"
                             f"Никнейм: {nickname}\n"
                             f"ПК/Мб: {device}\n"
                             f"Сервер: {server}\n"
                             f"Редстоун: {redstone}\n"
                             f"ПвП/ПвЕ: {pvp_pve}\n"
                             f"Часов в день: {playtime}\n"
                             f"Учеба: {study}\n"
                             f"Тимейты: {teammates}\n"
                             f"Страна: {country}\n"
                             f"Возраст: {age}\n"
                             f"Интернет: {internet}\n"
                             f"Контакт: {contact}", reply_markup=keyboard)
    return "Заявка отправлена!"

@dp.callback_query_handler(lambda c: c.data == 'accept')
async def process_accept(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="Заявка принята!")
    await bot.send_message(callback_query.from_user.id, "Вы были приняты в команду!")

@dp.callback_query_handler(lambda c: c.data == 'reject')
async def process_reject(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="Заявка отклонена!")
    await bot.send_message(callback_query.from_user.id, "Ваша заявка отклонена.")

async def on_start():
    # Запуск Flask приложения в отдельном потоке
    from threading import Thread

    def run_flask():
        app.run(host='0.0.0.0', port=5000)

    thread = Thread(target=run_flask)
    thread.start()

    # Запуск бота
    await dp.start_polling()

if __name__ == '__main__':
    # Запуск через asyncio
    asyncio.run(on_start())

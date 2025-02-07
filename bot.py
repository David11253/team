import telebot
from flask import Flask, request

TOKEN = '7705095327:AAGTdo2oXWMACVl8cufB-gYzDNzD4UxTUiU'  # Твой токен
bot = telebot.TeleBot(TOKEN)

# Flask-сервер для обработки данных формы
app = Flask(__name__)

# ID твоей группы в Telegram
GROUP_ID = '-1002428849357'

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form
        nickname = data['nickname']
        device = data['device']
        server = data['server']
        redstone = data['redstone']
        playstyle = data['playstyle']
        playtime = data['playtime']
        study = data['study']
        teammates = data['teammates']
        country = data['country']
        age = data['age']
        internet = data['internet']
        contact = data['contact']

        message = f"""
        Новая заявка на вступление:
        Никнейм: {nickname}
        ПК или Мб: {device}
        На каком сервере играете: {server}
        Редстоун: {redstone}/10
        ПвП или ПвЕ: {playstyle}
        Часы игры в день: {playtime}
        Учеба: {study}
        Тимейты: {teammates}
        Страна: {country}
        Возраст: {age}
        Интернет: {internet}/10
        Контакт: {contact}
        """
        
        bot.send_message(GROUP_ID, message)
        bot.send_poll(GROUP_ID, "Голосование: принять заявку?", options=["Принять", "Отказать"], is_anonymous=True)

        return "Заявка отправлена!"

if __name__ == '__main__':
    app.run(debug=True)

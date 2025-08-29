# zuhfacadebimport os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

# Твой токен и ID группы
BOT_TOKEN = "7592969962:AAFavNdgwxlyzf-oPRvVeDNLOzfPFjWrjbw"
GROUP_CHAT_ID = "-100XXXXXXXXXX"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route("/" + BOT_TOKEN, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running", 200

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Заявка принята.")

# Установка вебхука
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://<твое_приложение>.herokuapp.com/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
ot-webhook.

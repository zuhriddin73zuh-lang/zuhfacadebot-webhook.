# bot_webhook.py
import os
from flask import Flask, request
import telebot

# Вставлены твой токен и ID группы
TOKEN = "7592969962:AAFavNdgwxlyzf-oPRvVeDNLOzfPFjWrjbw"
GROUP_ID = -1002116032863

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Простая логика приёма заявки (имя -> телефон -> комментарий) ---
def ask_phone(message, name):
    msg = bot.send_message(message.chat.id, "📞 Введите ваш номер телефона:")
    bot.register_next_step_handler(msg, get_phone, name)

def ask_comment(message, name, phone):
    msg = bot.send_message(message.chat.id, "✍️ Кратко опишите задачу/адрес:")
    bot.register_next_step_handler(msg, finish_request, name, phone)

def get_phone(message, name):
    phone = message.text.strip()
    ask_comment(message, name, phone)

def finish_request(message, name, phone):
    comment = message.text.strip()
    bot.send_message(message.chat.id, "✅ Спасибо! Ваша заявка принята.")
    try:
        from datetime import datetime, timezone, timedelta
        tz = timezone(timedelta(hours=5))
        now = datetime.now(tz).strftime("%d.%m.%Y %H:%M")
    except:
        now = ""
    forward = (
        "🆕 Новая заявка\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📝 Комментарий: {comment}\n"
        f"👤 От: @{message.from_user.username or '—'} (id {message.from_user.id})\n"
        f"⏰ {now} (Asia/Tashkent)"
    )
    try:
        bot.send_message(GROUP_ID, forward)
    except Exception as e:
        # если пересылка в группу не удалась — сообщим в личку отправителю
        try:
            bot.send_message(message.chat.id, f"Ошибка при пересылке в группу: {e}")
        except:
            pass

@bot.message_handler(commands=['start'])
def cmd_start(message):
    msg = bot.send_message(message.chat.id, "👋 Как вас зовут?")
    bot.register_next_step_handler(msg, handle_name)

def handle_name(message):
    name = message.text.strip()
    if not name:
        bot.send_message(message.chat.id, "Введите имя.")
        return
    ask_phone(message, name)

# --- Webhook endpoints ---
@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/')
def sethook():
    # При деплое Render задаёт RENDER_EXTERNAL_URL — используем её
    url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("SERVICE_URL") or ""
    if url:
        webhook_url = url.rstrip('/') + '/' + TOKEN
        try:
            bot.remove_webhook()
        except:
            pass
        bot.set_webhook(url=webhook_url)
        return f"Webhook set: {webhook_url}", 200
    return "No external URL set", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    # локально для теста
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
s
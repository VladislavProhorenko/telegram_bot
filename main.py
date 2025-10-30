import google.generativeai as genai
import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# === Налаштування токенів ===
TELEGRAM_TOKEN = "8265303363:AAFnwypiKOsEdE2DWTMFtHaxAXuk3XVns3E"
GEMINI_API_KEY = "AIzaSyDWkgsNJYHTk0k-q4zCrxuB_daLkzj7Cyk"

# === Підключення до Google Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# === Меню ===
main_menu = [["Студент", "IT-технології"],
             ["Контакти", "Відповідь від нейромережі"]]

# Меню для режиму чат-нейромережа
chat_menu = [["Повернутися до головного меню"]]

# === /start ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Привіт! Я бот з підтримкою Google Gemini.\nОберіть дію нижче:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )
    context.user_data["chat_mode"] = False
    context.user_data["chat_history"] = []

# === Виклик Gemini ===
def ask_gemini(prompt, history):
    try:
        # прибрано "Відповідати українською"
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print("[Gemini ERROR]", e)
        return "⚠️ Помилка з боку Gemini API."

# === Обробка повідомлень ===
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    # Основне меню
    if text == "Студент":
        update.message.reply_text("👨‍🎓 Студент: Прохоренко В.Д.\nГрупа: ІО-з21")
        context.user_data["chat_mode"] = False

    elif text == "IT-технології":
        update.message.reply_text("💡 Python, HTML, CSS, JavaScript")
        context.user_data["chat_mode"] = False

    elif text == "Контакти":
        update.message.reply_text("📞 Телефон: +380674573478\n📧 Email: vladprokhorenko721@gmai.com")
        context.user_data["chat_mode"] = False

    elif text == "Відповідь від нейромережі":
        update.message.reply_text(
            "✍️ Напиши свій запит — я відповім через Google Gemini:",
            reply_markup=ReplyKeyboardMarkup(chat_menu, resize_keyboard=True)
        )
        context.user_data["chat_mode"] = True
        context.user_data["chat_history"] = []

    # Кнопка повернення з режиму чат
    elif text == "Повернутися до головного меню":
        update.message.reply_text(
            "⬆️ Повернулися до головного меню:",
            reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        )
        context.user_data["chat_mode"] = False
        context.user_data["chat_history"] = []

    # Режим чат з нейромережею
    elif context.user_data.get("chat_mode", False):
        update.message.chat.send_action(action="typing")
        try:
            history = context.user_data.get("chat_history", [])
            reply = ask_gemini(text, history)
            history.append({"role": "user", "parts": [text]})
            history.append({"role": "model", "parts": [reply]})
            context.user_data["chat_history"] = history
            update.message.reply_text(reply)
        except Exception as e:
            update.message.reply_text("❌ Сталася помилка при зверненні до Gemini.")
            print(e)
    else:
        update.message.reply_text("Виберіть пункт меню ⬆️")

# === Основна функція ===
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🚀 Бот запущено (Gemini API online)")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

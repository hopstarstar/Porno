
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ТВОЙ ТОКЕН
TOKEN = "8107838667:AAGy84WVK1nLT35XS8QIb0MzrN0hoIgxfQw"
# ТВОЙ АДМИН ID
ADMIN_ID = 70056447225

# Словник для зберігання запитів від користувачів
pending_requests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Напиши номер товару, і ми перевіримо його статус.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    # Користувач пише номер товару
    pending_requests[user_id] = text
    
    # Відповідаємо користувачу
    await update.message.reply_text("Зачекайте, йде перевірка...")

    # Відправляємо тобі як адміну повідомлення про новий запит
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новий запит від {user_id}: {text}\nВідповісти можна командою /reply {user_id} ваш_текст")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Адмін відправляє відповідь
    if update.message.chat_id != ADMIN_ID:
        await update.message.reply_text("У вас немає прав використовувати цю команду.")
        return

    try:
        user_id = int(context.args[0])
        response_text = ' '.join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=response_text)
        await update.message.reply_text("Відповідь надіслано успішно!")
    except Exception as e:
        await update.message.reply_text(f"Помилка: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Помилка: {context.error}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_error_handler(error_handler)

print("Бот запущений!")
app.run_polling()


import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import datetime

TOKEN = "8010735696:AAHuJEAHWVZxvrqEcp6ZwxNebgjHJXNNeU0"

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Список привычек
HABITS = [
    "Утренняя зарядка",
    "Медитация",
    "Нет сахара",
    "Прогулка 30 мин",
    "Сон до 22:30",
    "1 час без телефона",
    "Время для себя"
]

user_data = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data[user.id] = {"progress": {}}
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я помогу тебе отслеживать полезные привычки.
"
        "Каждый день буду спрашивать, что ты выполнил."
    )

# Команда /habits
async def habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(habit, callback_data=habit)] for habit in HABITS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Отметь, что ты сделал сегодня:", reply_markup=reply_markup)

# Обработка нажатий
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    habit = query.data
    today = datetime.date.today().isoformat()

    if user_id not in user_data:
        user_data[user_id] = {"progress": {}}
    if today not in user_data[user_id]["progress"]:
        user_data[user_id]["progress"][today] = []

    if habit not in user_data[user_id]["progress"][today]:
        user_data[user_id]["progress"][today].append(habit)
        await query.edit_message_text(text=f"Записал: {habit} на {today}")
    else:
        await query.edit_message_text(text=f"{habit} уже была отмечена сегодня.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("habits", habits))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()

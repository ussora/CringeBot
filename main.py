from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging


# Инициализация логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Словарь для хранения участников и их баллов
participants = {}

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот для начисления баллов кринжа. Используй команду /add_points <количество> для начисления баллов.")

# Функция для регистрации участника
def register(update: Update, context: CallbackContext) -> None:
    participants[update.message.chat_id] = 0
    update.message.reply_text("Вы успешно зарегистрированы!")

# Функция для добавления баллов участнику
def add_points(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id in participants:
        points = int(context.args[0])
        if points in [5, 10, 15]:
            participants[update.message.chat_id] += points
            update.message.reply_text(f"Баллы успешно начислены. Текущий баланс: {participants[update.message.chat_id]}")
        else:
            update.message.reply_text("Допустимые значения для начисления баллов: 5, 10, 15.")
    else:
        update.message.reply_text("Вы не зарегистрированы. Используйте команду /register для регистрации.")

# Функция для вывода текущих лидеров по количеству баллов
def show_leaderboard(update: Update, context: CallbackContext) -> None:
    sorted_participants = sorted(participants.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"{i + 1}. {member}: {points}" for i, (member, points) in enumerate(sorted_participants)])
    update.message.reply_text(f"Текущий рейтинг:\n{leaderboard}")

def main() -> None:
    updater = Updater("7132891038:AAFZit7NX0SV2ZuI3esRPeBpunPlLRk5jDc", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("register", register))
    dispatcher.add_handler(CommandHandler("add_points", add_points))
    dispatcher.add_handler(CommandHandler("leaderboard", show_leaderboard))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

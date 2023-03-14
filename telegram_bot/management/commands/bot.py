from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot

from telegram_bot.problems import problem, lst


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

        # Handle '/start' and '/help'
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)


    @bot.message_handler(commands=['list'])
    def get_problems(message):
        msg = lst.start()
        bot.reply_to(message=message, text=msg)


    @bot.message_handler(commands=['problems'])
    def get_problems(message):
        msg = problem.start()
        bot.reply_to(message=message, text=msg)


    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, message.text)


    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота






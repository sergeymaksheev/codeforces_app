import random

from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot, types

from main_app.models import Problem, Tag


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):

    def __init__(self) -> None:
        self.selected_tag_name = None

    help = 'Implemented to Django application telegram bot setup command'


    @bot.message_handler(commands=['помощь', 'старт'])
    def send_welcome(message):
        bot.reply_to(message, """\
            Здравствуйте
            Я готов выдать вам список задач. Просто выбери подходящую тему и проблему!\
            """)
            

    @bot.message_handler(commands=['темы'])
    def tags_list(message):
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='Список тем', callback_data='get_tags')
        kb.add(btn)
        bot.send_message(message.chat.id, message.text, reply_markup=kb)

    def get_tag(self):
        queryset = Tag.objects.all()
        lst = list(queryset)
        kb = types.InlineKeyboardMarkup(row_width=1)    
        for tag in lst:
            btn = types.InlineKeyboardButton(text=tag.name, callback_data=f"get_rating/{tag.name}")
            kb.add(btn)
        return kb
    
    @bot.callback_query_handler(func=lambda callback: callback.data)
    def check_callback_data(callback):
        if callback.data == 'get_tags':
            kb = command.get_tag()
            bot.send_message(callback.message.chat.id, 'Вы нажали на список тем', reply_markup=kb)
        else:
            command.selected_tag_name = callback.data.split('/')[1]
            callback.data = callback.data.split('/')[0]
            if callback.data == 'get_rating':
                result = bot.send_message(callback.message.chat.id, 'Введите сложность задачи')
                send = bot.reply_to(result, 'Введите сложность задачи')
                bot.register_next_step_handler(send, command.get_problems)


    def get_url(self, problem: Problem) -> str:
        return f"https://codeforces.com/problemset/problem/{problem.contest_id}/{problem.index}"


    def get_problems(self, message):
        rating = int(message.text)
        tag_name = self.selected_tag_name

        queryset = Problem.objects.filter(tags__name=str(tag_name), rating__gte=rating)
        lst = list(queryset)
        if len(lst) > 10:
            lst = random.sample(lst, 10)
        print(lst)
        kb = types.InlineKeyboardMarkup(row_width=1)    
        for problem in lst:
            url = command.get_url(problem)
            btn = types.InlineKeyboardButton(text=problem.name, url=url)
            kb.add(btn)
        bot.send_message(message.chat.id, 'Вы нажали на список тем', reply_markup=kb)

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота


command = Command()


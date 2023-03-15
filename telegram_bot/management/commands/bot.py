from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot, types

from telegram_bot.problems import problem, lst
from main_app.models import Problem


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

        # Handle '/start' and '/help'
    # @bot.message_handler(commands=['help', 'start'])
    # def send_welcome(message):
    #     bot.reply_to(message, """\
    # Hi there!
    # I am here to get you math problems. Just choose tags and raiting for problems!\
    # """)

    tag_list = ['темы', 'теги', 'список тем', 'список тегов']

    

    @bot.message_handler(regexp=f'{tag_list}')
    def start(message):
        sent = bot.reply_to(message, 'Пожалуйста, введите название темы')
        bot.register_next_step_handler(sent, get_tag)


    @bot.message_handler(regexp=f'{tag_list}')
    def echo_message(message):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Кнопка1')
        btn2 = types.KeyboardButton(text='Кнопка2')
        kb.add(btn1, btn2)
        bot.reply_to(message, 'выберете тему', reply_markup=kb)

    
    @bot.message_handler(commands=['call'])
    def echo_message(message):
        kb = types.ReplyKeyboardMarkup(row_width=1)
        btn1 = types.KeyboardButton(text='Кнопка1')
        btn2 = types.KeyboardButton(text='Кнопка2')
        kb.add(btn1, btn2)
        bot.reply_to(message, 'выберете тему', reply_markup=kb)


    @bot.message_handler(commands=['start'])
    def echo_message(message):
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Кнопка1', url='https://pytba.readthedocs.io/en/latest/quick_start.html')
        btn2 = types.InlineKeyboardButton(text='Кнопка2', url='https://pytba.readthedocs.io/en/latest/quick_start.html')
        kb.add(btn1, btn2)
        bot.reply_to(message, 'выберете тему', reply_markup=kb)


    @bot.message_handler(commands=['switch'])
    def echo_message(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        switch = types.InlineKeyboardButton(text='Выбрать чат', switch_inline_query='/start')
        markup.add(switch)
        bot.reply_to(message, 'выберете тему', reply_markup=markup)


    @bot.message_handler(commands=['start'])
    def get_problems(message):
        msg = lst.start()
        bot.reply_to(message=message, text=msg)


    @bot.message_handler(commands=['problems'])
    def get_problems(message):
        msg = problem.start()
        bot.reply_to(message=message, text=msg)

    # @bot.message_handler(commands=['test'])
    # def get_tag(message):
    #     tag_lst = list(lst.get_list())
    #     for tag in tag_lst:
    #         if tag == message:
    #             return message.text == str(tag)

    
    # @bot.message_handler(func=get_tag)
    # def echo_message(message):
    #     bot.reply_to(message, 'hi')


    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, 'Введите корректную команду, например "темы" или "список тем"')


    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота



def get_url(problem: Problem) -> str:
    return f"https://codeforces.com/problemset/problem/{problem.contest_id}/{problem.index}"


def get_tag(message):
    queryset = Problem.objects.filter(tags__name=str(message.text))[:10]
    lst = list(queryset)
    kb = types.InlineKeyboardMarkup(row_width=1)    
    for problem in lst:
        url = get_url(problem)
        btn = types.InlineKeyboardButton(text=problem.name, url=url)
        kb.add(btn)

    bot.reply_to(message, message.text, reply_markup=kb)


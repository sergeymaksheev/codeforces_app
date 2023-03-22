import random
import telebot
from typing import Dict

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Max, Min
from telebot import TeleBot, types

from main_app.models import Problem, Tag


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):

    def __init__(self) -> None:
        self.selected_tag_name = None
        self.some_list = []

    help = 'Implemented to Django application telegram bot setup command'

    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Перезапуск бота"),
        telebot.types.BotCommand("/tags", "Выбор темы"),
    ])


    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        """Start working with bot. Get a first menu: Choose tags"""

        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 
                         text="""<b>Добро пожаловать!!!</b>
                        Я бот, который выдает задачи по указанной теме и сложности. Я готов выдать вам список задач. 
                        Пожалуйста, выберите подходящую тему и сложность!
                        """, 
                        parse_mode='HTML',
                        reply_markup=command.create_menu()
                        )


    @staticmethod
    def create_menu() -> types.InlineKeyboardMarkup:
        """Create menu for TG bot: Button, when you push on it, 
        create calls and start get_tags function"""

        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Список тем', callback_data='get_tags')
        markup.add(btn)
        return markup


    @bot.message_handler(commands=['tags'])
    def command_tag(message):
        """Receive commmand /tags from BotCommand and start get_tags function"""

        kb = command.get_tags()
        bot.send_message(message.chat.id, 'Вы нажали на список тем', reply_markup=kb)
    

    @staticmethod
    def get_tags() -> types.InlineKeyboardMarkup:
        """Get tags from db and create list with tags"""

        queryset = Tag.objects.all()
        lst = list(queryset)
        kb = types.InlineKeyboardMarkup(row_width=1)    
        for tag in lst:
            btn = types.InlineKeyboardButton(text=tag.name, callback_data=f"get_rating/{tag.name}")
            kb.add(btn)
        return kb


    @staticmethod
    def get_rating(tag_name) -> Dict[str, int]:
        """Aggregate min and max rating for problems when you chose tag and create callback in get_tags function"""

        max_value =  Problem.objects.filter(tags__name=tag_name).aggregate(Max('rating'))
        min_value =  Problem.objects.filter(tags__name=tag_name).aggregate(Min('rating'))
        return min_value, max_value


    @bot.callback_query_handler(func=lambda callback: callback.data)
    def check_callback_data(callback):
        """Check all callback calls from functions"""

        if callback.data == 'get_tags':
            kb = command.get_tags()
            bot.send_message(callback.message.chat.id, 'Вы нажали на список тем', reply_markup=kb)

        else:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)  # clear previos callback calls
            command.selected_tag_name = callback.data.split('/')[1]
            callback.data = callback.data.split('/')[0]
            if callback.data == 'get_rating':

                min_value, max_value = command.get_rating(command.selected_tag_name)
                min_value = min_value.get('rating__min')
                max_value = max_value.get('rating__max')
                
                send = bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=f'Вы выбрали тему {command.selected_tag_name}\
                    Введите сложность задачи: от {min_value} до {max_value}',
                    reply_markup='',
                )
                bot.register_next_step_handler(
                    message=send, 
                    min_value=min_value, 
                    max_value=max_value, 
                    callback=command.get_tagname,
                )

    
    @staticmethod
    def get_url(problem: Problem) -> str:
        """Ger url for chosen problem from codenames web server"""

        return f"https://codeforces.com/problemset/problem/{problem.contest_id}/{problem.index}"


    def get_tagname(self, message, min_value, max_value):
        try:
            tag_name = self.selected_tag_name
            rating = int(message.text)
            if rating < min_value or rating > max_value:
                raise  ValueError()
        except ValueError:
            send = bot.send_message(message.chat.id, f'Введите целое число, от {min_value} до {max_value} ')
            bot.register_next_step_handler(message=send, min_value=min_value, max_value=max_value, callback=command.get_tagname)
            btn = types.InlineKeyboardButton('Назад к списку тем', callback_data='get_tags')
            kb = types.InlineKeyboardMarkup()
            kb.add(btn)
            bot.edit_message_reply_markup(message.chat.id, text='Вы можете попробовать заново выбрать тему', reply_markup=kb)
        else:
            command.get_problems(tag_name=tag_name, rating=rating, message=message)


    @staticmethod
    def get_problems(tag_name, rating, message):
        """Get problems from db when your chose tag and rating. 
        Get ten random problems. if less than ten problems in db, give available problems"""
        
        queryset = Problem.objects.filter(tags__name=str(tag_name), rating__gte=rating)
        lst = list(queryset)
        if len(lst) > 10:
            lst = random.sample(lst, 10)
        kb = types.InlineKeyboardMarkup()
        for problem in lst:
            url = command.get_url(problem)
            btn = types.InlineKeyboardButton(text=problem.name, url=url)
            kb.add(btn)

        bot.send_message(message.chat.id, f'Список задач по теме {tag_name} со сложностью {rating} и выше', reply_markup=kb)
        kb2 = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton('Назад к списку тем', callback_data='get_tags')
        kb2.add(back)
        bot.send_message(message.chat.id, 'Вы можете попробовать заново выбрать тему', reply_markup=kb2)
    
    
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, text='Пожалуйста, выберите необходимую команду')


    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота


command = Command()
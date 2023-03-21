import random

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


    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, text="""
                <b>Добро пожаловать!!!</b>
                Я бот, который выдает задачи по указанной теме и сложности. Я готов выдать вам список задач. Пожалуйста, выберите подходящую тему и сложность!
                """, 
                parse_mode='HTML',
                reply_markup=command.create_menu()
                )

        
    @staticmethod
    def create_menu() -> types.InlineKeyboardMarkup:
        '''Создаём меню для TG бота'''
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Список тем', callback_data='get_tags')
        markup.add(btn)
        return markup
            

    def get_tag(self):
        queryset = Tag.objects.all()
        lst = list(queryset)
        kb = types.InlineKeyboardMarkup(row_width=1)    
        for tag in lst:
            btn = types.InlineKeyboardButton(text=tag.name, callback_data=f"get_rating/{tag.name}")
            kb.add(btn)
        return kb
    

    @staticmethod
    def get_rating(tag_name):
        max_value =  Problem.objects.filter(tags__name=tag_name).aggregate(Max('rating'))
        min_value =  Problem.objects.filter(tags__name=tag_name).aggregate(Min('rating'))
        return min_value, max_value


    @bot.callback_query_handler(func=lambda callback: callback.data)
    def check_callback_data(callback):
        if callback.data == 'get_tags':
            kb = command.get_tag()
            #bot.send_message(callback.message.chat.id, 'Вы нажали на список тем', reply_markup=kb)
            bot.edit_message_reply_markup(
                    chat_id = callback.message.chat.id, 
                    message_id = callback.message.id, \
                    reply_markup = kb
                    )# удаляем кнопки у последнего сообщения
        else:
            command.selected_tag_name = callback.data.split('/')[1]
            callback.data = callback.data.split('/')[0]
            if callback.data == 'get_rating':

                min_value, max_value = command.get_rating(command.selected_tag_name)
                min_value = min_value.get('rating__min')
                max_value = max_value.get('rating__max')

                send = bot.edit_message_text(
                    f'Вы выбрали тему {command.selected_tag_name}\
                    Введите сложность задачи: от {min_value} до {max_value}',
                    chat_id=callback.message.chat.id,
                    message_id = callback.message.id,
                    reply_markup='')
                bot.register_next_step_handler(message=send, 
                                                min_value=min_value, 
                                                max_value=max_value, 
                                                callback=command.get_tagname
                                                )

    
    
    def get_url(self, problem: Problem) -> str:
        return f"https://codeforces.com/problemset/problem/{problem.contest_id}/{problem.index}"


    def get_tagname(self, message, min_value, max_value):
        ls = []
        ccc = message.text
        ls.append(ccc)
        print('/////////////', ls)
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
            #bot.send_message(message.chat.id, text='Вы можете попробовать заново выбрать тему', reply_markup=kb)
            bot.edit_message_reply_markup(message.chat.id, text='Вы можете попробовать заново выбрать тему', reply_markup=kb)
        else:
            command.get_problems(tag_name=tag_name, rating=rating, message=message)
        

    @staticmethod
    def get_problems(tag_name, rating, message):
        print('ddddddddddddddd', tag_name, rating)
        queryset = Problem.objects.filter(tags__name=str(tag_name), rating__gte=rating)
        lst = list(queryset)
        if len(lst) > 10:
            lst = random.sample(lst, 10)
        #print(lst)
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
        bot.reply_to(message, message.text)

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()								# Загрузка обработчиков
        bot.infinity_polling()											# Бесконечный цикл бота


command = Command()
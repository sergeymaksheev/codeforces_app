import logging
import requests

from bs4 import BeautifulSoup
from random import randint
from typing import Iterable, Optional

#from tgbot.handlers import static_text as st
from main_app.models import Problem, Tag

logger = logging.getLogger('default')


class Problems:

    def get_problems(self):

        return Problem.objects.all()[:10]


    @staticmethod
    def format_problem(problem: Problem) -> str:

        return f'*{problem}'
    
    def start(self) -> None:
        res = self.get_problems()
        return self.format_problem(problem=list(res)[0].name)

    
problem = Problems()


class List:

    def get_list(self):

        return Tag.objects.all()
    

    @staticmethod
    def format_list(lst: Tag) -> str:

        return f'*{lst}'
    

    def start(self) -> None:
        res = self.get_list()
        return self.format_list(lst=list(res))


lst = List()
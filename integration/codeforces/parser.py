from . provider import get_result
from main_app.models import Problem, Tag
from django.db import models


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def start_bulk_create(Entry:models.Model, list_to_create:list[models.Model], batch_size=1000)->None:
    for chunk in batch(list_to_create, batch_size):
        Entry.objects.bulk_create(chunk, batch_size=batch_size)
    

def get_problems(data: dict) -> list:
    return data.get('problems', [])
  

def get_problem_statistics(data:dict) -> list:
    return data.get('problemStatistics', [])


def get_problems_lst_and_tags():
    resp = get_result()
    problems = {(value.get('contestId'), value.get('index')): value for value in get_problems(data=resp)}
    statistics = {(value.get('contestId'), value.get('index')): value for value in get_problem_statistics(data=resp)}
    tags = []
    for key, problem in problems.items():
        tags += problem.get('tags', [])
        current_stat = statistics.get(key)
        if current_stat:
            problem.update(current_stat)
    return problems, set(tags)


def insert_new_tags(tags:list) -> None:
    tags_db = list(Tag.objects.values_list('name', flat=True))
    tags_to_create = []

    for item in tags:
        if item not in tags_db:
            tags_to_create.append(Tag(name=item))
    
    if tags_to_create:
        start_bulk_create(Entry=Tag, list_to_create=tags_to_create)


def insert_new_problems(problems:dict) -> None:
    problems_db = Problem.objects.all()
    problem_ids = [(value.contest_id, value.index) for value in list(problems_db)]
    problems_to_create = []

    for key, problem in problems.items():
        if key not in problem_ids:
            problems_to_create.append(
                Problem(
                    contest_id=problem.get('contestId'),
                    index = problem.get('index'),
                    name = problem.get('name'),
                    type = problem.get('type'),
                    points = problem.get('points'),
                    rating = problem.get('rating'),
                    solved_count = problem.get('solvedCount')
                )
            )

    if problems_to_create:
        start_bulk_create(Entry=Problem, list_to_create=problems_to_create)


def insert_tags_to_problems(problems) -> None:
    tags_id = Tag.objects.values('id', 'name')
    print('/////////dfdsfds////', tags_id)
    for problem in problems.values():
        print('ggggggfvfdvdsadagggsdcdcsdgggggg', problem)





        
# a2 = Article(headline='NASA uses Python')
# >>> a2.save()
# >>> a2.publications.add(p1, p2)
# >>> a2.publications.add(p3)




def start_problems_task():
    problems, tags = get_problems_lst_and_tags()
    insert_new_tags(tags=list(tags))
    insert_new_problems(problems=problems)
    insert_tags_to_problems(problems=problems)

# from integration.codeforces.parser import start_problems_task
# start_problems_task()
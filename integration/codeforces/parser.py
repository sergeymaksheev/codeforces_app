from . provider import get_problems
from main_app.models import Problem, Tag


def get_data():
    problems_lst = get_problems().get('problems', [])
    problem_objects = Problem.objects.all()
    tag_objects = Tag.objects.all()
    problem_ids = [(p.contest_id, p.index) for p in problem_objects]
    tag_ids = [t.name for t in tag_objects]
    
    tags_to_create = []

    problems_to_create = []
    
    
    for problem in problems_lst:
        for tag in problem.get('tags', []):
            if tag not in tags_to_create:
                tags_to_create.append(tag)
    
        key = (problem.get('contestId'), problem.get('index'))
        if key not in problem_ids:
            problems_to_create.append(Problem(name=problem.get('name'), ))
        
        
    return problems_to_create
        

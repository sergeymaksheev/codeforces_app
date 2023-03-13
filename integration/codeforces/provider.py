import httpx
import json

# def get_result() -> dict:
#     with httpx.Client(base_url='https://codeforces.com/api/') as client:
#         endpoint = 'problemset.problems'
#         resp = client.get(url=endpoint)
#         return json.loads(resp.content.decode("utf-8")).get('result', {})



def get_result() -> dict:
    with open(  
            "/home/sergey/projects/codeforces_app/response_from_server/res.json", "r", encoding="utf-8"
            ) as f:
        return json.loads(f.read().encode('utf-8'))



def get_problems(data: dict) -> list:
    return data.get('problems', [])
  

def get_problem_statistics(data:dict) -> list:
    return data.get('problemStatistics', [])


def get_problems_lst():
    resp = get_result()
    problems = {(value.get('contestId'), value.get('index')): value for value in get_problems(data=resp)}
    statistics = {(value.get('contestId'), value.get('index')): value for value in get_problem_statistics(data=resp)}
    for key, problem in problems.items():
        current_stat = statistics.get(key)
        if current_stat:
            problem.update(current_stat)
    print(problems)
    return problems

    



        










# def get_tags():
#     problems_lst = get_problems()
#     tags = [item.get('tags') for item in problems_lst]
#     tag_l = []
#     for item in tags:
#         tag_l.extend(item)
#         print(tag_l)



get_problems_lst()
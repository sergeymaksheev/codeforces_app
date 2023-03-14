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

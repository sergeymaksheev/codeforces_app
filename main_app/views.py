from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView

from integration.codeforces.parser import get_data
from main_app.serializers import ProblemsSerializer

# Create your views here.
def index(request):
    res = get_data()
    context = {'problems_to_create': res}
    return render(
        request,
        'index.html',
        context=context)


class ProblemsView(APIView):
    pass


    
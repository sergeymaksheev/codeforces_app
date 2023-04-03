from django.http import HttpResponse

def status(request) -> HttpResponse:
    return HttpResponse('<h1>Status OK</h1>')
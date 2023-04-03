from django.urls import path

from main_app.views import status

urlpatterns = [
    path("", status)
]

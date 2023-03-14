from django.urls import path
from . import views




urlpatterns = [
    #path('', views.index, name='index'),
    path('api/', views.TagsAPIView.as_view()),
    path('apil/', views.TagListAPIView.as_view()),
]
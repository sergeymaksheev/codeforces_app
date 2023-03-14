from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination

from main_app.serializers import ProblemSerializer
from main_app.models import Problem


class ProblemListAPIView(generics.ListCreateAPIView):
    
    queryset = Problem.objects.filter(rating=2000).filter(tags__name='graphs')[:10]
    serializer_class = ProblemSerializer


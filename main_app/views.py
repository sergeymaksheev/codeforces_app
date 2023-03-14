from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from rest_framework import generics

from main_app.serializers import TagsSerializer
from main_app.models import Tag

# # Create your views here.
# def index(request):
#     res = get_data()
#     context = {'problems_to_create': res}
#     return render(
#         request,
#         'index.html',
#         context=context)


class TagsAPIView(APIView):
    

    def post(self, request):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):


            return Response(data=serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class TagListAPIView(generics.ListAPIView):
    
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()




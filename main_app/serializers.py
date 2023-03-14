from rest_framework import serializers

from main_app.models import Tag, Problem


# from integration.codeforces.provider import get_problems

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


from rest_framework import serializers

from integration.codeforces.provider import get_problems


class ProblemsSerializer(serializers.Serializer):
    contest_id = serializers.IntegerField()
    index = serializers.CharField()
    name  = serializers.CharField()
    type = serializers.CharField()
    points = serializers.FloatField()
    rating = serializers.IntegerField()
    solved_count = serializers.IntegerField()
    tags = serializers.CharField()
    created = serializers.DateTimeField()


class ProblemsLstSerializer(serializers.Serializer):
    problems_lst = get_problems()   #.get('problems', [])
    problems = problems_lst
    problems = ProblemsSerializer(many=True)



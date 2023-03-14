from django.db import models

# Create your models here.
from enum import Enum

from django.core.validators import MinValueValidator

# Create your models here.
class TypeEnum(Enum):
    PROGRAMMING = "PROGRAMMING"
    QUESTION = "QUESTION"


class Tag(models.Model):
    """This is class representing a topics models"""
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Problem(models.Model):
    """This is class representing a problems"""
    contest_id = models.IntegerField(validators=[MinValueValidator(0)])
    index = models.CharField(max_length=200)
    name  = models.CharField(max_length=200)
    type = models.CharField(
        max_length=200,
        choices=[
        (TypeEnum.PROGRAMMING, ('PROGRAMMING')),
        (TypeEnum.PROGRAMMING, ('QUESTION')),
        ]
    )
    points = models.FloatField(validators=[MinValueValidator(0.0)], null=True)
    rating = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    solved_count = models.IntegerField(validators=[MinValueValidator(0)])
    tags = models.ManyToManyField(Tag, related_name='tags')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
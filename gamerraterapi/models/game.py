"""Game model module"""
from gamerraterapi.models import category
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """ Game database model"""
    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=75)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    num_of_players = models.IntegerField()
    est_time = models.IntegerField()
    age_rec = models.IntegerField()

    @property
    def AvgRating(self):
        return self.__AvgRating

    @AvgRating.setter
    def AvgRating(self, value):
        self.__AvgRating = value
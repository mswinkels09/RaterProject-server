"""Game model module"""
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """ Game database model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=75)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    num_of_players = models.IntegerField()
    est_time = models.IntegerField()
    age_rec = models.IntegerField()
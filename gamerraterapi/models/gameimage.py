"""GameImage model module"""
from django.db import models

class GameImage(models.Model):
    """ GameImage database model"""

    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    image = models.CharField(max_length=75)
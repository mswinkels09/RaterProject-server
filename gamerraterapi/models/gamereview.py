"""GameReview model module"""
from django.db import models
from django.contrib.auth.models import User

class GameReview(models.Model):
    """ GameReview database model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    review = models.CharField(max_length=75)

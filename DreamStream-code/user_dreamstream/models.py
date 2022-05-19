from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FavMovies(models.Model):
    title = models.CharField(max_length=100)
    fav_user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    poster_img = models.CharField(max_length=1000, default=None)
    def __str__(self):
        return f'{self.fav_user} :: {self.title} :: {self.poster_img}'
from distutils.command.upload import upload
from email.policy import default
from signal import default_int_handler
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
# Create your models here.

class FavMovies(models.Model):
    title = models.CharField(max_length=100)
    fav_user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    poster_img = models.CharField(max_length=1000, default=None)
    
    def __str__(self):
        return f'{self.fav_user} :: {self.title} :: {self.poster_img}'

class ProfileDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="default.jpg", blank=True, upload_to='static/dreamstream/images/pfp/')

    def __str__(self):
        return f"{self.user}'s Profile info"
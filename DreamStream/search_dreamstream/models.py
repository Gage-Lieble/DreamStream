from django.db import models

# Create your models here.

class TitleSearch(models.Model):
    search = models.CharField(max_length=50)

    def __str__(self):
        return f"search{self.search}"
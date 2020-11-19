from django.db import models

# Create your models here.

class Movie(models.Model):
    movie_title = models.CharField(max_length=100)
    
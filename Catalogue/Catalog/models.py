from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    developers = models.CharField(max_length=128)
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    cover = models.ImageField(upload_to = "static/Catalog/game_icons/", height_field=None, width_field=None, max_length=None)
    marks = models.IntegerField(default=0)
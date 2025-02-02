from django.contrib import admin
from .models import Game

# Register your models here.
class GameManager(admin.ModelAdmin):
    list_display = ("id","title","developers","description","release_date","cover")

admin.site.register(Game, GameManager)
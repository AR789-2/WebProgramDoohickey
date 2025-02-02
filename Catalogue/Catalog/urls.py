from . import views
from django.urls import path

urlpatterns = [
    path("",views.index, name="index"),
    path("list/",views.list_of_games, name="list_of_games"),
    path("<int:game_id>",views.gamepage, name="game"),
    path("<int:game_id>/<str:rank>",views.gameranked, name="rank")
]
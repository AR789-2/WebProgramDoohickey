from django.shortcuts import render
from .models import Game
from django.http import HttpResponseRedirect
from django.urls import reverse

#Setup Ranking Rules
ranks = {
    'D': 1,
    'C': 3,
    'B': 5,
    'A': 8,
    'S': 10,
    'V': 12,
}

def resetmarks():
    for g in Game.objects.all():
        g.marks = 0
        g.save()

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        'TitleTag': 'Home',
        'Games': Game.objects.all()
    })

def list_of_games(request):
    return render(request, 'list.html', {
        'TitleTag': 'List of Games',
        'Games': Game.objects.all().order_by('-marks')
    })

def gamepage(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game.html', {
        'TitleTag': game.title,
        'game': game,
        'ranks': ranks
    })

def gameranked(request, game_id, rank): #USE SESSIONS TO PREVENT MULTI-RANKING
    sess = f"G_{game_id}"
    game = Game.objects.get(id=game_id)
    print(f"{game.title} has been ranked a {rank}. The Game got {ranks[rank]} points!")
    try:
        SecondVote = request.session[sess]
        if SecondVote:
            game.marks -= request.session[sess]
            print("This User has already voted, reducting points...")
            print(f"-{request.session[sess]}")
    except:
        print("All Good")
    game.marks += ranks[rank]
    request.session[sess] = ranks[rank]
    print(game.marks)
    game.save()
    return HttpResponseRedirect(reverse("game", args=str(game.id)))
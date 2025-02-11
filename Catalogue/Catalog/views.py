from django.shortcuts import render
from .models import Game
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

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

class NewTaskForm(forms.Form):
    task = forms.CharField(label='New Task')
    priority = forms.IntegerField(label='priority', min_value=1, max_value=5)

def index(request):
    l = []
    for g in Game.objects.all():
        l.append(g)
    top_3 = []
    while len(top_3) < 3:
        lead = None
        hs = -2
        for g in l:
            if g.marks > hs:
                if not g in top_3:
                    lead = g
                    hs = g.marks
        top_3.append(lead)
        print(lead.title)
        #l.remove(dx)

    run_2 = [top_3[1],top_3[2]]

    return render(request, 'index.html', {
        'TitleTag': 'Home',
        'Games': Game.objects.all(),
        "No_1": top_3[0],
        'Run_2': run_2,
    })

def list_of_games(request):
    return render(request, 'list.html', {
        'TitleTag': 'List of Games',
        'Games': Game.objects.all().order_by('-marks')
    })

def gamepage(request, game_id):
    sess = f"G_{game_id}"
    game = Game.objects.get(id=game_id)
    prevvote = 'None'
    try:
        SecondVote = request.session[sess]
        if SecondVote:
            # Find that rank for display
            pv = [key for key, val in ranks.items() if val == request.session[sess]]
            prevvote = str(pv)[2]
            print(prevvote)
    except:
        prevvote = 'None'
    return render(request, 'game.html', {
        'TitleTag': game.title,
        'game': game,
        'ranks': ranks,
        'cur_rank': prevvote
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
            if request.session[sess] == ranks[rank]:
                rank = None
    except:
        print("All Good")
    if rank is not None:
        game.marks += ranks[rank]
        request.session[sess] = ranks[rank]
    else:
        request.session[sess] = None
    print(game.marks)
    game.save()
    return HttpResponseRedirect(reverse("game", args=str(game.id)))

def search(request):
    state = request.GET.get('fname', None)
    results = Game.objects.filter(title__contains=state)

    return render(request, "list.html", {
        'TitleTag': f'Search for: {state}',
        'Games': results
    })
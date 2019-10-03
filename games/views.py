from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'games/games.html')


def game(request):
    return render(request, 'games/game.html')

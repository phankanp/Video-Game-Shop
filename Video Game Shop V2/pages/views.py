from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from games.models import Game
# Create your views here.


class HomePageView(ListView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()

        homepage_games_list = []

        for i in range(12):
            homepage_games_list.append(games[i])

        context = {
            'games': homepage_games_list
        }

        return render(self.request, 'home.html', context)

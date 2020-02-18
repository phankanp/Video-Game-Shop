from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect
from django import template

from games.models import Game, WishList
from orders.models import Order, OrderItem
# Create your views here.


class HomePageView(ListView):
    def get(self, request, *args, **kwargs):

        games = Game.objects.all()

        wished = WishList.objects.all().filter(user=self.request.user)

        games_to_show = 0

        if (len(games) < 9):
            games_to_show = len(games)
        else:
            games_to_show = 9

        homepage_games_list = []

        for i in range(games_to_show):
            homepage_games_list.append(games[i])

        wished_games = []

        for i in wished.iterator():
            wished_games.append(i.wished_game.title)

        context = {
            'games': homepage_games_list,
            'wished_games': wished_games,

        }

        return render(self.request, 'pages/index.html', context)

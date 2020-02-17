from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect


from games.models import Game
from orders.models import Order
# Create your views here.


class HomePageView(ListView):
    def get(self, request, *args, **kwargs):
        games = Game.objects.all()
        order = None
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
        except ObjectDoesNotExist:
            pass

        games_to_show = 0

        if (len(games) < 9):
            games_to_show = len(games)
        else:
            games_to_show = 9

        homepage_games_list = []

        for i in range(games_to_show):
            homepage_games_list.append(games[i])

        context = {
            'games': homepage_games_list,
            'order': order,
        }

        return render(self.request, 'pages/index.html', context)

from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from games.models import Game

# Create your views here.


class PlatformView(ListView):
    def get(self, request, *args, **kwargs):
        PLATFORM_CHOICES = {
            'X': 'Xbox',
            'PS': 'PS4',
            'S': 'Switch',
            'PC': 'PC',
        }
        try:
            platform_name = self.kwargs['platform_name']

            games = Game.objects.all().filter(platform=platform_name)

            context = {
                'games': games,
                'platform': PLATFORM_CHOICES[platform_name]
            }
            return render(self.request, 'platform_page.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Unable to load platform page")

            return redirect("/")


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game.html"


class SearchResultsListView(ListView):
    model = Game
    context_object_name = 'game_list'
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Game.objects.filter(
            Q(title__icontains=query)
        )

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from .render import Render

import rawgpy
import requests
import json
import math
import stripe

PLATFORM_CHOICES = {
    'X': 'Xbox',
    'PS': 'PS4',
    'S': 'Switch',
    'PC': 'PC',
}


class HomeView(ListView):
    def get(self, request, *args, **kwargs):
        try:
            platform_name = self.kwargs['platform_name']

            games = Game.objects.all().filter(platform=platform_name)

            context = {
                'games': games,
                'platform': PLATFORM_CHOICES[platform_name]
            }
            return render(self.request, 'games/games.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Unable to load platform page")

            return redirect("/")

    # model = Game
    # template_name = "games/games.html"


class GameDetailView(DetailView):
    model = Game

    template_name = "games/game_detail.html"

    def get_context_data(self, **kwargs):
        """ Get single game details from RAWG.io """
        rawg = rawgpy.RAWG("games")
        results = rawg.search(self.get_object().title)
        g = results[0]
        g.populate()

        """ Get screenshots for a single game """
        screenshot_url = f"https://api.rawg.io/api/games/{g.id}/screenshots"
        response = requests.get(screenshot_url)
        json_object = json.loads(response.text)
        screenshot_results = json_object['results']
        screenshots = []

        for i in range(len(screenshot_results)):
            screenshots.append(screenshot_results[i].get('image'))

        """ Get trailer for a single game """
        trailer_url = f"https://api.rawg.io/api/games/{g.id}/movies"
        trailer_response = requests.get(trailer_url)
        trailer_json_object = json.loads(trailer_response.text)
        trailer_results = trailer_json_object['results']

        """ get_context_data let you fill the template context """
        context = super().get_context_data(**kwargs)
        context['platform'] = PLATFORM_CHOICES[self.get_object().platform]
        context['developers'] = g.developers
        context['rating'] = math.floor(g.rating)
        context['screenshots'] = screenshots

        if trailer_results:
            context['trailer'] = trailer_results[0].get('data').get('max')

        return context

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

from .render import Render
import stripe
import json
from django.http import HttpResponse
from django.http import JsonResponse


class HomeView(ListView):
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
            return render(self.request, 'games/games.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Unable to load platform page")

            return redirect("/")

    # model = Game
    # template_name = "games/games.html"


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game.html"

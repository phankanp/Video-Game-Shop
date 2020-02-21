from django import template
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, WishList
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from .render import Render

from orders.models import Order

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


class PlatformView(ListView):

    def get(self, request, *args, **kwargs):

        order = None

        globalOrderQTY = 0

        wished_games = []

        if request.user.is_authenticated:
            wished = WishList.objects.all().filter(user=self.request.user)

            for i in wished.iterator():
                wished_games.append(i.wished_game.title)

            try:
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                globalOrderQTY = order.get_total_cart_quantity()
            except ObjectDoesNotExist:
                pass

        try:
            platform_name = self.kwargs['platform_name']

            games = Game.objects.all().filter(platform=platform_name)

            context = {
                'games': games,
                'platform': PLATFORM_CHOICES[platform_name],
                'order': order,
                'globalOrderQTY': globalOrderQTY,
                'wished_games': wished_games,
            }

            return render(self.request, 'games/games.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Unable to load platform page")

            return redirect("/")


class WishListView(LoginRequiredMixin, ListView):

    template_name = 'wishlist.html'

    def get(self, request, *args, **kwargs):

        order = None

        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)

        except ObjectDoesNotExist:
            pass

        try:
            wished = WishList.objects.all().filter(user=self.request.user)

            wished_games = []

            for i in wished.iterator():
                wished_games.append(i.wished_game.title)

            context = {
                'games': wished,
                'wished_games': wished_games,
                'order': order,
            }

            return render(self.request, 'wishlist.html', context)
        except ObjectDoesNotExist:
            return redirect("/")


class CartSummaryView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order,
            }

            return render(self.request, 'shopping_cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Shopping Cart is empty")

            return redirect("/")


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


class SearchResultsListView(ListView):

    model = Game

    context_object_name = 'game_list'

    template_name = 'search_results.html'

    def get_queryset(self):  # new

        query = self.request.GET.get('q')

        return Game.objects.filter(
            Q(title__icontains=query)
        )


@login_required
def add_remove_to_wishlist(request, pk):

    game = get_object_or_404(Game, pk=pk)

    msg = ''

    added = None

    check_if_wished = WishList.objects.filter(
        user=request.user, wished_game=game)

    if not check_if_wished:
        wished_game, created = WishList.objects.get_or_create(
            wished_game=game, user=request.user)
        msg = f'{game.title} was added to your wish list'
        added = True
    else:
        WishList.objects.filter(user=request.user, wished_game=game).delete()
        msg = f'{game.title} was removed from your wish list'
        added = False

    if request.is_ajax():

        json_data = {
            'msg': msg,
            'added': added
        }

        return JsonResponse(json_data)

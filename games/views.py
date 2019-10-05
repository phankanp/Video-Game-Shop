from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Game, OrderItem, Order
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

# def game_list(request, platform_name):

#     context = {
#         'games': Game.objects.filter(platform=platform_name)
#     }

#     return render(request, 'games/games.html', context)


class HomeView(ListView):
    model = Game
    template_name = "games/games.html"


# def single_game(request, game_id):
#     context = {
#         'game': Game.objects.get(pk=game_id)
#     }

#     return render(request, 'games/game.html', context)

class GameDetailView(DetailView):
    model = Game
    template_name = "games/game.html"


def add_to_cart(request, pk):
    game = get_object_or_404(Game, pk=pk)

    order_item, created = OrderItem.objects.get_or_create(
        game=game, user=request.user, ordered=False)

    order_query = Order.objects.filter(user=request.user, ordered=False)

    if order_query.exists():
        order = order_query[0]

        if order.games.filter(game_id=game.pk).exists():

            order_item.quantity += 1

            order_item.save()

            messages.info(request, f'{game.title} was added to your cart')
        else:
            messages.info(request, f'{game.title} was added to your cart')

            order.games.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.games.add(order_item)
        messages.info(request, f'{game.title} was added to your cart')
    return redirect("single_game", pk=pk)


def remove_from_cart(request, pk):
    game = get_object_or_404(Game, pk=pk)

    order_query = Order.objects.filter(user=request.user, ordered=False)

    if order_query.exists():

        order = order_query[0]

        if order.games.filter(game_id=game.pk).exists():
            order_item = OrderItem.objects.filter(
                game=game, user=request.user, ordered=False)[0]

            if order_item.quantity > 1:
                order.games.remove(order_item)

                order_item.quantity -= 1

                order_item.save()

                messages.info(
                    request, f'{game.title} was removed from your cart')
                return redirect("single_game", pk=pk)
            elif order_item.quantity == 1:
                order_item.delete()
                messages.info(
                    request, f'{game.title} was removed from your cart')

            if not order.games.exists():
                order.delete()
                return redirect("single_game", pk=pk)

        else:
            messages.info(request, f'{game.title} is not in your cart')
            return redirect("single_game", pk=pk)
    else:
        messages.info(request, 'No active orders')
        return redirect("single_game", pk=pk)

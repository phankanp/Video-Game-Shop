from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from .models import Game, OrderItem, Order, Coupon
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages

from .forms import CheckoutForm, CouponForm
from .models import Address


class HomeView(ListView):
    model = Game
    template_name = "games/games.html"


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game.html"


class CartSummaryView(View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'shopping_cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Shopping Cart is empty")

            return redirect("/")


def checkout_view(request):

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():

                shipping_main_address = form.cleaned_data.get('address')
                shipping_optional_address = form.cleaned_data.get(
                    'optional_address')
                shipping_country = form.cleaned_data.get('country')
                shipping_zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if '' not in (shipping_main_address, shipping_country, shipping_zip):
                    shipping_address = Address(
                        user=request.user,
                        address=shipping_main_address,
                        optional_address=shipping_optional_address,
                        country=shipping_country,
                        zip=shipping_zip
                    )
                    shipping_address.save()

                    order.shipping_address = shipping_address
                    order.save()
                else:
                    messages.warning(
                        request, "Please fill in the required shipping address fields")
                    return redirect('checkout')

                if (same_billing_address != True):
                    billing_main_address = form.cleaned_data.get('billing_address')
                    billing_optional_address = form.cleaned_data.get('billing_optional_address')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if '' not in (billing_main_address, billing_country, billing_zip):
                        billing_address = Address(
                            user=request.user,
                            address=billing_main_address,
                            optional_address=billing_optional_address,
                            country=billing_country,
                            zip=billing_zip
                        )
                    billing_address.save()

                    order.billing_address = billing_address
                    order.save()
                else:
                    billing_address = order.shipping_address
                    billing_address.save()

                    order.billing_address = billing_address
                    order.save() 

                return redirect('checkout')
            messages.warning(request, "Please fill in the required shipping address fields")

            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.warning(request, "Shopping Cart is empty")

            return redirect("shopping_cart")
    else:
        form = CheckoutForm()
        coupon_form = CouponForm()
        order2 = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'checkout.html', {'form': form, 'coupon': coupon_form, 'order': order2})

@require_POST
def add_coupon_view(request):
    
    form = CouponForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data.get('code')

        try:
            coupon = Coupon.objects.get(code__iexact=code)

            order = Order.objects.get(user=request.user, ordered=False)

            order.coupon = coupon

            order.save()

            messages.success(request, "Successfully added coupon")
            
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.info(request, "No active order")
            
            return redirect("checkout")    

@login_required
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
            return redirect("shopping-cart")
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


@login_required
def remove_from_cart(request, pk):
    game = get_object_or_404(Game, pk=pk)

    order_query = Order.objects.filter(user=request.user, ordered=False)

    if order_query.exists():

        order = order_query[0]

        if order.games.filter(game_id=game.pk).exists():
            order_item = OrderItem.objects.filter(
                game=game, user=request.user, ordered=False)[0]

            if order_item.quantity > 1:
                # order.games.remove(order_item)

                order_item.quantity -= 1

                order_item.save()

                messages.info(
                    request, f'{game.title} was removed from your cart')
                return redirect("shopping-cart")
            elif order_item.quantity == 1:
                order_item.delete()
                messages.info(
                    request, f'{game.title} was removed from your cart')

            if not order.games.exists():
                order.delete()
                return redirect("shopping-cart")

        else:
            messages.info(request, f'{game.title} is not in your cart')
            return redirect("single_game", pk=pk)
    else:
        messages.info(request, 'No active orders')
        return redirect("single_game", pk=pk)

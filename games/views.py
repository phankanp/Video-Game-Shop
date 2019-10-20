from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Game, OrderItem, Order, Coupon, Payment
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

from .render import Render
import stripe
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import CheckoutForm, CouponForm
from .models import Address


# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY



class HomeView(ListView):
    def get(self, request, *args, **kwargs):
        PLATFORM_CHOICES = {
            'X': 'Xbox',
            'PS': 'PS4',
            'S': 'Switch',
            'PC': 'PC',
            'M': 'Mobile'
        }
        try:
            platform_name =  self.kwargs['platform_name']
       
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


class CartSummaryView(LoginRequiredMixin, View):
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

class OrdersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.all().filter(user=self.request.user).filter(ordered=True)
            context = {
                'orders': order
            }
            return render(self.request, 'orders.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Shopping Cart is empty")

            return redirect("/")

def payment_view(request):

    if request.method == 'POST':
        order = Order.objects.get(user=request.user, ordered=False)
        
        token = request.POST.get('stripeToken')
      
        try: 
            charge = stripe.Charge.create(
                amount=int(order.get_total_cart_price() * 100),
                currency='usd',
                description='Order charge',
                source=token,
            )
            
            payment = Payment()
            payment.stripe_charge_id = charge.id
            payment.user = request.user
            payment.amount = charge.amount / 100
            payment.save()

            order_items = order.games.all()
            order_items.update(ordered=True)
            for game in order_items:
                game.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(request, "Order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err  = body.get('error', {})

            messages.error(request, f"{err.get('message')}")
            return redirect("/games/checkout")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate limit error")
            return redirect("/games/checkout")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid parameters error")
            return redirect("/games/checkout")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Stripe authentication error")
            return redirect("/games/checkout")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Network communication error")
            return redirect("/games/checkout")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "Something went wrong. Charge did not go through, please try again!")
            return redirect("/games/checkout")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "Code Error")



def checkout_view(request):

    if request.method == 'POST' and request.is_ajax():

        form = CheckoutForm(request.POST)

        print(form)
       
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            
            if form.is_valid():
               
                shipping_main_address = form.cleaned_data.get('address')
                shipping_optional_address = form.cleaned_data.get(
                    'optional_address')
                shipping_country = form.cleaned_data.get('country')
                shipping_zip = form.cleaned_data.get('zip')
                shipping_city = form.cleaned_data.get('city')
                shipping_state = form.cleaned_data.get('state')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')
                
                print(shipping_state + '*****************************')

                if '' not in (shipping_main_address, shipping_country, shipping_zip, shipping_city):
                    shipping_address = Address(
                        user=request.user,
                        address=shipping_main_address,
                        optional_address=shipping_optional_address,
                        country=shipping_country,
                        zip=shipping_zip,
                        city=shipping_city,
                        state=shipping_state
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
                    billing_city = form.cleaned_data.get('billing_city')
                    billing_state = form.cleaned_data.get('billing_state')

                    if '' not in (billing_main_address, billing_country, billing_zip, billing_city):
                        billing_address = Address(
                            user=request.user,
                            address=billing_main_address,
                            optional_address=billing_optional_address,
                            country=billing_country,
                            zip=billing_zip,
                            city=billing_city,
                            state=billing_state
                        )
                    billing_address.save()

                    order.billing_address = billing_address
                    order.save()
                else:
                    billing_address = order.shipping_address
                    billing_address.save()

                    order.billing_address = billing_address
                    order.save() 
                
                return JsonResponse({"success":True}, status=200)
            #     return redirect('checkout')
            
            messages.warning(request, "Please fill in the required shipping address fields")

            return JsonResponse({"success":False}, status=400)
            # return redirect("checkout")
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
    return redirect("games_list", platform_name=game.platform)


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



def admin_order_pdf(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    context = {
        'order': order
    }
    
    return Render.render('invoice.html', context)
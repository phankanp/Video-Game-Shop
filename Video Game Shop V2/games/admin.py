from django.contrib import admin

from games.models import Game
from orders.models import OrderItem, Order, Coupon
# Register your models here.

admin.site.register(Game)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
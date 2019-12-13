from django.contrib import admin

from .models import Game, OrderItem, Order, Coupon
# Register your models here.

admin.site.register(Game)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)
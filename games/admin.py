from django.contrib import admin

from .models import Game, OrderItem, Order
# Register your models here.

admin.site.register(Game)
admin.site.register(OrderItem)
admin.site.register(Order)

from django.contrib import admin

from .models import OrderItem, Order, Coupon
# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Coupon)

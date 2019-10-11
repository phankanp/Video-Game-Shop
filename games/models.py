from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.


PLATFORM_CHOICES = (
    ('X', 'Xbox'),
    ('PS', 'PS4'),
    ('S', 'Switch'),
    ('PC', 'PC'),
    ('M', 'Mobile')
)


class Game(models.Model):
    title = models.CharField(max_length=100)

    description = models.CharField(max_length=1000,  default="")

    release_date = models.DateField()

    developer = models.CharField(max_length=100)

    price_per_unit = models.DecimalField(
        max_digits=5, decimal_places=2, default=60.00)

    platform = models.CharField(
        choices=PLATFORM_CHOICES, default="", max_length=2)

    genre_tages = ArrayField(models.CharField(
        max_length=200),  default=list, blank=True)

    box_art = models.CharField(max_length=100)

    def get_add_to_cart_url(self):
        return reverse("add_to_cart", kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove_from_cart", kwargs={
            'pk': self.pk
        })

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    ordered = models.BooleanField(default=False)

    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.game.title}'

    def get_total_cart_item_price(self):
        return self.game.price_per_unit * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    games = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField(timezone.now())

    ordered = models.BooleanField(default=False)

    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)

    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)

    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_cart_price(self):
        x = 0
        
        for order_item in self.games.all():
            x += order_item.game.price_per_unit * order_item.quantity
        
        if self.coupon:
            x -= self.coupon.amount    
        
        return x

    def get_total_cart_quantity(self):
        x = 0
        
        for order_item in self.games.all():
            x += order_item.quantity
       
        return x


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    address = models.CharField(max_length=1000,  default="")

    optional_address = models.CharField(max_length=1000,  default="")

    country = CountryField(multiple=False)

    zip = models.CharField(max_length=10,  default="")

    address_type = models.CharField(max_length=8)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField( max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.code.upper()

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField( max_digits=5, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
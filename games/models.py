from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

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


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    games = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField(timezone.now())

    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

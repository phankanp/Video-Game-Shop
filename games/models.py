from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django_countries.fields import CountryField


PLATFORM_CHOICES = (
    ('X', 'Xbox'),
    ('PS', 'PS4'),
    ('S', 'Switch'),
    ('PC', 'PC'),
)


class Game(models.Model):

    title = models.CharField(max_length=100)

    description = models.CharField(max_length=1000,  default="")

    release_date = models.DateField()

    developers = ArrayField(models.CharField(
        max_length=200),  default=list, blank=True)

    price_per_unit = models.DecimalField(
        max_digits=5, decimal_places=2, default=59.99)

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

    def get_add_remove_to_wishlist_url(self):
        return reverse("add_remove_to_wishlist", kwargs={
            'pk': self.pk
        })

    def get_add_to_wishlist_url(self):
        return reverse("add_to_wishlist", kwargs={
            'pk': self.pk
        })

    def get_remove_from_wishlist_url(self):
        return reverse("remove_from_wishlist", kwargs={
            'pk': self.pk
        })

    def get_platform_name(self, platform):
        return PLATFORM_CHOICES[platform]

    def __str__(self):
        return self.title


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    wished_game = models.ForeignKey(Game, on_delete=models.CASCADE)

    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wished_game.title

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

    def get_platform_name(self, platform):
        return PLATFORM_CHOICES[platform]

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

    ORDER_CHOICES = (
    ('p', 'Payment Recieved'),
    ('pe', 'Pending'),
    ('pa', 'Packing'),
    ('s', 'Shippped'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    games = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(auto_now_add=True)

    ordered_date = models.DateTimeField(timezone.now())

    ordered = models.BooleanField(default=False)

    order_status = models.CharField(
        max_length=2,
        choices=ORDER_CHOICES,
        default='pe',
    )

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
    
    def get_generate_invoice_url(self):
        return reverse("invoice", kwargs={
            'pk': self.pk
        })


class Address(models.Model):
    STATE_CHOICES = (("AL","AL"),("AK","AK"),("AZ","AZ"),("AR","AR"),("CA","CA"),("CO","CO"),("CT","CT"),("DE","DE"),("FL","FL"),("GA","GA"),("HI","HI"),("ID","ID"),("IL","IL"),("IN","IN"),("IA","IA"),("KS","KS"),("KY","KY"),("LA","LA"),("ME","ME"),("MD","MD"),("MA","MA"),("MI","MI"),("MN","MN"),("MS","MS"),("MO","MO"),("MT","MT"),("NE","NE"),("NV","NV"),("NH","NH"),("NJ","NJ"),("NM","NM"),("NY","NY"),("NC","NC"),("ND","ND"),("OH","OH"),("OK","OK"),("OR","OR"),("PA","PA"),("RI","RI"),("SC","SC"),("SD","SD"),("TN","TN"),("TX","TX"),("UT","UT"),("VT","VT"),("VA","VA"),("WA","WA"),("WV","WV"),("WI","WI"),("WY","WY"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    address = models.CharField(max_length=1000,  default="")

    optional_address = models.CharField(max_length=1000,  default="")

    country = CountryField(multiple=False)

    city = models.CharField(max_length=50,  default="")

    zip = models.CharField(max_length=10,  default="")

    address_type = models.CharField(max_length=8)

    state = models.CharField(
    max_length=2,
    choices=STATE_CHOICES,
    default='',
    )

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
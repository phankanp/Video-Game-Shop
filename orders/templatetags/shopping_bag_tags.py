from django import template
from orders.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        quesry_set = Order.objects.filter(user=user, ordered=False)

        if quesry_set.exists():
            return quesry_set[0].get_total_cart_quantity()
        else:
            return 0

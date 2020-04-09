from django.urls import path

from orders import views


urlpatterns = [
    path('invoice/<int:pk>/', views.AdminOrderPdf.as_view(), name='invoice'),
    path('', views.OrdersView.as_view(), name='orders'),
    path('checkout/payment', views.payment_view, name='payment'),
    path('checkout-coupon/apply', views.add_coupon_view, name='checkout-coupon'),
    path('checkout', views.checkout_view, name='checkout'),
    path('shopping-cart', views.CartSummaryView.as_view(), name='shopping-cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove-item-from-cart/<int:pk>/',
         views.remove_item_from_cart, name='remove_item_from_cart')
]

from django.urls import path

from . import views

# app_name = "games"

urlpatterns = [
    path('invoice/<int:pk>/', views.admin_order_pdf, name='invoice'),
    path('orders', views.OrdersView.as_view(), name='orders'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='single_game'),
    path('checkout/payment', views.payment_view, name='payment'),
    path('checkout-coupon/apply', views.add_coupon_view, name='checkout-coupon'),
    path('checkout', views.checkout_view, name='checkout'),
    path('shopping-cart', views.CartSummaryView.as_view(), name='shopping-cart'),
    path('<str:platform_name>', views.HomeView.as_view(), name='games_list'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),


]
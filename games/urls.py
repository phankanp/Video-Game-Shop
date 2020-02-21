from django.urls import path

from . import views

# app_name = "games"

urlpatterns = [
    path('wishlist', views.WishListView.as_view(), name='wish_list'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    path('<str:platform_name>', views.PlatformView.as_view(), name='games_list'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='single_game'),
    path('wishlist/<int:pk>/', views.add_remove_to_wishlist,
         name='add_remove_to_wishlist'),
]

from django.urls import path

from . import views

# app_name = "games"

urlpatterns = [
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    path('<str:platform_name>', views.HomeView.as_view(), name='games_list'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='single_game'),
]

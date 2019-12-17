from django.urls import path

from games import views

urlpatterns = [
    path('search/', views.SearchResultsListView.as_view(), name='search_results'),
    path('<str:platform_name>', views.PlatformView.as_view(), name='games_list'),
]

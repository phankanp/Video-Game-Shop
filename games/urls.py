from django.urls import path

from . import views

# app_name = "games"

urlpatterns = [
    path('<str:platform_name>', views.HomeView.as_view(), name='games_list'),
]

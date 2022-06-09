from django.urls import path
from league.views import home

app_name = "league"

urlpatters = [
    path('', home, name="home")
]
from django.urls import path
from league.views import home

app_name = "league"

urlpatterns = [
    path("", home, name="home")
]
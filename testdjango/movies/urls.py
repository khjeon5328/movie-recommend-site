from django.urls import path
from . import views


app_name= "movies"

urlpatterns = [
    path('', views.movies, name="movies"),
    path('movieDetail/', views.movieDetail),
    path('test/', views.test),
]

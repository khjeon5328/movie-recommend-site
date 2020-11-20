from django.urls import path
from . import views


app_name= "movies"

urlpatterns = [
    path('', views.movies, name="movies"),
    # path('make/', views.makeMovie, name=""),
    path('detail/', views.moviedetail, name="moviedetail"),
    path('home/', views.home, name="home"),
    
]

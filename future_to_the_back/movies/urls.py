from django.urls import path
from . import views


app_name= "movies"

urlpatterns = [
    path('', views.home, name="home"),
    path('movies/', views.movies, name="movies"),
    path('search/', views.search, name="search"),
    # path('make/', views.makeMovie, name=""),
    path('<int:movie_id>/', views.moviedetail, name="moviedetail"),
    path('article/', views.article, name="article"),
]

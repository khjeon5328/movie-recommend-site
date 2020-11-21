from django.urls import path
from . import views


app_name= "movies"

urlpatterns = [
    path('', views.movies, name="movies"),
    # path('make/', views.makeMovie, name=""),
    path('<int:movie_id>/', views.moviedetail, name="moviedetail"),
    path('home/', views.home, name="home"),
    path('article/', views.article, name="article"),
    
]

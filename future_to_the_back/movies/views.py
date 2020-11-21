from django.shortcuts import render

import requests
import json
from pprint import pprint
from .models import MovieDetail, Movie
from pprint import pprint
# Create your views here.


def movies(request):
    movies = []
    movies = Movie.objects.filter(target_dt='20180428')
    movies_detail = []
    for i in movies:
        movies_detail.append(MovieDetail.objects.get(movie=i))

    context = {
        'movies_detail' : movies_detail,
    }
    return render(request, 'movies/movies.html', context)


def moviedetail(request, movie_id):
    movie_detail = MovieDetail.objects.filter(pk=movie_id)
    print(movie_detail)
   
    context = {
        'movie_detail':movie_detail[0],
    }

    return render(request, 'movies/moviedetail.html', context)


def home(request):

    return render(request, 'movies/home.html')



def article(request):

    return render(request, 'movies/_article.html')
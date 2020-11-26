from django.shortcuts import render, redirect

import requests
import json
from pprint import pprint
from .models import MovieDetail, Movie
from pprint import pprint
from reviews.models import Review, Comment
from reviews.forms import Review, CommentForm
from django.contrib import messages

# Create your views here.


def movies(request):
    # home에서 받은 정보로 dt만들기
    month = request.GET.get('month')
    year = request.GET.get('year')
    day = request.GET.get('day')

    target_dt= year + month + day

    movies = []
    # movies = Movie.objects.filter(target_dt='20180428')
    movies = Movie.objects.filter(target_dt=target_dt)
    if not movies:
        messages.error(request, '😢Sorry there are no movie data at that time🐱‍🚀')
        return redirect('movies:home')

    movies_detail = []
    for i in movies:
        movies_detail.append(MovieDetail.objects.get(movie=i))

    first_rank_movie_score = movies_detail[0].netizen_score + movies_detail[0].special_score
    first_rank_movie_idx = 1
    for i in range(1, len(movies_detail)):
        score = movies_detail[i].netizen_score + movies_detail[i].special_score
        if score > first_rank_movie_score:
            first_rank_movie_score = score
            first_rank_movie_idx = i
    context = {
        'movies_detail' : movies_detail,
        'hidden_movie' : movies_detail[first_rank_movie_idx],
        'rank_1_movie_title' : movies_detail[0].movie.movie_name,
    }
    return render(request, 'movies/movies.html', context)



def moviedetail(request, movie_id):
    movie_detail = MovieDetail.objects.filter(pk=movie_id)
    movie = MovieDetail.objects.get(pk=movie_id)
    reviews = movie.review_set.all()
    context = {
        'movie_detail':movie_detail[0],
        'reviews':reviews,
        'comment_form' : CommentForm(),
    }
    return render(request, 'movies/moviedetail.html', context)




def home(request):
    return render(request, 'movies/home.html')


def article(request):
    return render(request, 'movies/_article.html')
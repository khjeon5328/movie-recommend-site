from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import (
    Review, 
    Comment
)
from .forms import (
    ReviewForm, 
    CommentForm
)
import json
from django.http import JsonResponse
from movies.models import MovieDetail, Movie
# Create your views here.


def reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_review(request, movie_id):
    movie = get_object_or_404(MovieDetail, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.movie = movie
            review.save()
            return redirect('movies:moviedetail', movie_id)
    else:
        form = ReviewForm()
    context = {
        'form' : form,
        'form_name': "새로운 리뷰 작성",
        'button_name' : 'POST',
    }
    return render(request, 'accounts/form.html', context)


@login_required
@require_http_methods(['GET'])
def detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        'review': review,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'reviews/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        if request.user == review.author:
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('movies:moviedetail', review.movie_id)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form' : form,
        'form_name': "글 수정",
        'button_name' : 'UPDATE',
    }
    return render(request, 'accounts/form.html', context)


@login_required
@require_http_methods(['POST'])
def delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.author:
        review.delete()
    return redirect('movies:moviedetail', review.movie_id)


@login_required
@require_http_methods(['POST'])
def create_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comment_form = CommentForm(json.loads(request.body.decode('utf-8')))
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.author = request.user
        comment.save()
        data = {
            'content' : comment.content,
            'author' : str(comment.author),
            'count' : review.comment_set.count(),
            'review_id' : review_id,
            'comment_id' : comment.id,
        }
        return JsonResponse(data)
    context = {
        'comment_form': comment_form,
        'review': review,
    }
    return render(request, 'reviews/detail.html', context)



@require_http_methods(['POST'])
def delete_comment(request, review_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        review = get_object_or_404(Review, pk=review_id)
        if request.user == comment.author:
            comment.delete()
            data = {
                'is_delete' : True,
                'count': review.comment_set.count(),
              
            }
            return JsonResponse(data)
    return render(request, 'reviews/detail.html')


@login_required
def like(request, review_id):
    review = get_object_or_404(Review, pk=review_id) 
    if request.user.is_authenticated:
        me = request.user
        if review.like_users.filter(pk=me.pk).exists():
            review.like_users.remove(me)
            is_like = False
        else:
            review.like_users.add(me)
            is_like = True
        data = {
            'is_like': is_like,
            'like_count': review.like_users.count(),
        }
        return JsonResponse(data)
    return redirect('movies:moviedetail', review.movie_id)
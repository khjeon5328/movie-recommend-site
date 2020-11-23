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
# Create your views here.


def reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('reviews:reviews')
    else:
        form = ReviewForm()
    context = {
        'form' : form
    }
    return render(request, 'reviews/create.html', context)


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
    if request.user == review.author:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', review_id)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form' : form,
    }
    return render(request, 'reviews/update.html', context)


@login_required
@require_http_methods(['POST'])
def delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.author:
        review.delete()
    return redirect('reviews:reviews')


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
            print(data)
            return JsonResponse(data)
    return render(request, 'reviews/detail.html')

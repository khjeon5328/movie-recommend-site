from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm

# Create your views here.

def reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/reviews.html', context)

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

def detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    context = {
        'review': review
    }
    return render(request, 'reviews/detail.html', context)


def update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
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

def delete(request, review_id):
    get_object_or_404(Review, pk=review_id).delete()
    return redirect('reviews:reviews')
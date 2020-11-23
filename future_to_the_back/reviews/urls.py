from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.reviews, name='reviews'),
    path('<int:movie_id>/create/', views.create_review, name='create_review'),
    path('<int:review_id>/', views.detail, name='detail'),
    path('<int:review_id>/update/', views.update, name='update'),
    path('<int:review_id>/delete/', views.delete, name='delete'),
    path('<int:review_id>/comments/', views.create_comment, name='create_comment'),
    path('<int:review_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]

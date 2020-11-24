from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/image/', views.profile_image, name='profile_image'),
    path('<str:username>/follow/', views.follow, name='follow'),
]

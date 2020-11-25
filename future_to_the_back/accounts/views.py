from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomUserProfileChangeForm
)
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods, require_POST

from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse

from django.contrib import messages
from random import *

# Create your views here.
# def index(request):
#     return render(request, 'accounts/index.html')





# @require_http_methods(['GET', 'POST'])
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('accounts:index')
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request,user)
#             messages.info(request, 'signup success')
#             return redirect(request.GET.get('next') or 'movies:home')
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form' : form,
#         'form_name': "회원가입",
#         'button_name' : 'SIGN UP',
#     }
#     return render(request, 'accounts/form.html', context)





@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.profile_image :
                base = '../static/images/'
                color = ['blue', 'dblue', 'ivory', 'orange','pink','purple','red','violet','yellow']
                rest = '-leather.jpg'
                idx = randint(0, len(color)-1)
                profiledefault = base + color[idx]+ rest
                user.profile_image = profiledefault
                user.save()
            auth_login(request,user)
            messages.info(request, 'signup success')
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form,
        'form_name': "회원가입",
        'button_name' : 'SIGN UP',
    }
    return render(request, 'accounts/form.html', context)





@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print(request.GET.get('next'))
            messages.info(request, 'login success')
            return redirect(request.GET.get('next') or 'movies:home')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
        'form_name': "로그인",
        'button_name' : 'LOG IN',
    }
    return render(request, 'accounts/form.html', context)


@login_required
# @require_POST
def logout(request):
    auth_logout(request)
    messages.info(request, 'logout success')
    print(request.GET.get('next'))
    return redirect(request.GET.get('next') or 'movies:home')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'updated success')
            return redirect('accounts:profile', request.user)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
        'form_name': "회원정보변경",
        'button_name' : 'UPDATE',
    }
    return render(request, 'accounts/form.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.info(request, 'change password success')
            return redirect('accounts:profile', request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
        'form_name': "비밀번호변경",
        'button_name' : 'UPDATE',
    }
    return render(request, 'accounts/form.html', context)



def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    context = {
        'person' : person,
        'form' : CustomUserProfileChangeForm()
    }
    return render(request, 'accounts/profile.html', context) 


@require_POST
def profile_image(request, username):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    form = CustomUserProfileChangeForm(request.POST, request.FILES,instance=request.user) 
    if form.is_valid():
        form.save()
    else:
        form =  CustomUserProfileChangeForm(instance=request.user)

    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person' : person,
        'form' : form,
    }
    return render(request, 'accounts/profile.html', context) 


@require_POST
def follow(request, username):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    you = get_object_or_404(get_user_model(), username=username)
    me = request.user
    print(you.followers)
    if me != you:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
            is_follower = False
        else:
            you.followers.add(me)
            is_follower = True
        data = {
            'user_name':username,
            'is_follower':is_follower,
            'follower_count' : you.followers.count(),
            'following_count' : you.followings.count(),
        }
        return JsonResponse(data)
    return redirect('accounts:profile', username)

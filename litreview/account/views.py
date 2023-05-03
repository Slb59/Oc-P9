from django.conf import settings
from django.shortcuts import render, redirect
from .forms import LoginUser, CreateUser
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def signup(request):
    """ post the signup data """
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,
                             'Compte créé avec succès pour ' + username)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'account/signup.html',
                  context={'form': form})


def logout_user(request):
    """logout the connected user and redirect to login page"""
    logout(request)
    return redirect('account:login')


def login_page(request):
    """ post the login form with username and password """
    if request.method == 'POST':
        form = LoginUser(request.POST, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.info(request,
                              "Bonjour, {user.username}! Vous êtes connecté")
                return redirect('review:feed')
            else:
                messages.info(request,
                              "utilisateur ou mot de passe non reconnu")
        else:
            messages.info(request,
                          "utilisateur ou mot de passe non reconnu")
    else:
        form = LoginUser()
    return render(request, 'account/login.html',
                  context={'form': form})

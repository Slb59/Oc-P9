from django.shortcuts import render
from .forms import LoginUser
from django.contrib.auth import login, authenticate
from django.contrib import messages


def login_page(request):

    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.info(request,
                              "Bonjour, {user.username}! Vous êtes connecté")
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

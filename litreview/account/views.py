from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import View
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
from django.db import IntegrityError

from .forms import LoginUser, CreateUser
from .forms import SubscriptionForm
from .models import UserFollows


def unsubscribe(request, id):
    """ remove the id user from the followed user """
    user = get_object_or_404(UserFollows, id=id)
    user.delete()
    return redirect('account:subscription')


class SubscriptionView(LoginRequiredMixin, View):
    """ 
        -> ask for a new subscription
        -> list followed users whith unscubscribe button
        -> list subscriber users whith unsubscribe button
    """
    form_class = SubscriptionForm
    template_name = 'account/subscription.html'

    def define_context(self, connected_user) -> dict:
        """ create a dict with the followed users 
        and subscriber users of the connected_user

        Args:
            connected_user (_type_): _description_

        Returns:
            dict: _description_
        """
        followed_users = UserFollows.objects.filter(user=connected_user)
        subscriber_users = UserFollows.objects.filter(
            followed_user=connected_user)
        return {'followed_users': followed_users,
                'subscriber_users': subscriber_users}

    def get(self, request):
        """ the get function for the request """
        form = self.form_class()
        context = self.define_context(request.user) | {'form': form}
        return render(
            request, self.template_name,
            context=context)

    def check_username(self, connected_user, username) -> str:
        """ check 
            -> if the connected user is not the user choice
            -> that the user choice exists
            -> that the user choice is not already in the followed list
        return the message corresponding to the cas encountered
        """
        message = ''
        try:
            followed_user = User.objects.get(username=username)
            if followed_user == connected_user:
                message = 'Allons, allons : vous ne pouvez vous suivre !'
            else:
                try:
                    user_follow = UserFollows.objects.create(
                        user=connected_user, followed_user=followed_user)
                    user_follow.save()
                    message = 'Utilisateur '\
                        + followed_user.username + ' ajouté'
                except IntegrityError:
                    message = 'Non, non: ' + followed_user.username\
                        + ' déjà suivi !'
        except Exception:
            message = username + ' ? Je ne connais pas ??'
        return message

    def post(self, request):
        """ the post function for the request """
        form = self.form_class(request.POST)
        if form.is_valid():
            # search the user object matching the user name entered
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            messages.info(request, self.check_username(request.user, username))
            context = self.define_context(request.user) | {'form': form}
            return render(
                request, self.template_name,
                context=context)

# class SignupPage(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('account:login')
#     template_name = 'account/signup.html'


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
        else:
            messages.info(request,
                          "Les données saisies sont invalides")
    return render(request, 'account/signup.html',
                  context={'form': form})


# def logout_user(request):
#     """logout the connected user and redirect to login page"""
#     logout(request)
#     return redirect(settings.LOGIN_URL)


class LoginPage(View):
    """ manage the login page get and post """
    form_class = LoginUser
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class()
        return render(
            request, self.template_name,
            context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.info(request,
                              f"Bonjour, {user.username}! Vous êtes connecté")
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.info(request,
                          "utilisateur ou mot de passe non reconnu")
        return render(
            request, self.template_name,
            context={'form': form})


# def login_page(request):
#     """ post the login form with username and password """
#     if request.method == 'POST':
#         form = LoginUser(request.POST, data=request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data['username'],
#                 password=form.cleaned_data['password'],
#             )
#             if user is not None:
#                 login(request, user)
#                 messages.info(request,
#                               "Bonjour, {user.username}! Vous êtes connecté")
#                 return redirect('review:feed')
#             else:
#                 messages.info(request,
#                               "utilisateur ou mot de passe non reconnu")
#         else:
#             messages.info(request,
#                           "utilisateur ou mot de passe non reconnu")
#     else:
#         form = LoginUser()
#     return render(request, 'account/login.html',
#                   context={'form': form})

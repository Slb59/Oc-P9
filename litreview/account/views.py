from django.conf import settings
from django.shortcuts import render, redirect
from .forms import LoginUser, CreateUser
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import View
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SubscriptionForm


class SubscriptionView(LoginRequiredMixin, View):
    form_class = SubscriptionForm
    template_name = 'account/subscription.html'

    def get(self, request):
        form = self.form_class()
        return render(
            request, self.template_name,
            context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # search the user object matching the user name entered
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            try:
                raise Exception
            except Exception:
                messages.info(request, 'utilisateur ' + username + ' inconnu')
                return render(
                    request, self.template_name,
                    context={'form': form})

            return render(
                request, self.template_name,
                context={'form': form})

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

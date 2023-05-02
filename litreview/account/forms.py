from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUser(AuthenticationForm):
    username = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'Mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class CreateUser(UserCreationForm):
    username = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Nom d'utilisateur"}))
    password1 = forms.CharField(
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(
        widget=forms.widgets.PasswordInput(
            attrs={'placeholder': 'Confirmer mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

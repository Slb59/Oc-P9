from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserFollows


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


class SubscriptionForm(ModelForm):

    username = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Nom d'utilisateur"}))

    # username = forms.CharField(
    #     widget=forms.ModelChoiceField(
    #         queryset=User.objects.all(),
    #         initial=0,
    #         required=True))

    # def __init__(self, *args, **kwargs):
    #     super(UserFollows, self).__init__(*args, **kwargs)
    #     self.fields['username'] =
    # forms.ModelChoiceField(queryset=User.objects.all())

    # username = forms.ModelChoiceField(
    #         queryset=User.objects.all())

    def __init__(self, user, *args, **kwargs):
        """ set the connected user """
        self.user = user
        # followed_users = UserFollows.objects.filter(user=self.user)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """ check
            -> if the connected user is not the user choice
            -> that the user choice exists
            -> that the user choice is not already in the followed list
        """
        user = self.cleaned_data['username']

        try:
            followed_user = User.objects.get(username=user)
            if followed_user == self.user:
                message = 'Vous ne pouvez pas vous suivre !'
                raise ValidationError(message)
            else:
                try:
                    user_follow = UserFollows.objects.create(
                        user=self.user, followed_user=followed_user)
                    user_follow.save()
                except IntegrityError:
                    message = 'Désolé: ' + followed_user.username\
                        + ' déjà suivi !'
                    raise ValidationError(message)
        except User.DoesNotExist:
            message = user + " n'est pas défini !"
            raise ValidationError(message)
        # except Exception:
            # message = user.username + ' ? Je ne connais pas ??'
            # raise ValidationError(message)
        # return message

        return user

    class Meta:
        model = UserFollows
        fields = ['username']
        # widgets = {'username': forms.ModelChoiceField(
        #     queryset=User.objects.all())}

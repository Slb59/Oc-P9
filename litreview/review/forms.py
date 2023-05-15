from django import forms
from django.forms import ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):

    title = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Titre"}))

    description = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': "Votre texte",
                "cols": "100"}))
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(ModelForm):

    headline = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Titre"}))
    
    body = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': "Votre critique",
                "cols": "100"}))
    
    rating = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'rate'}),
        initial=3,
        choices=[
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5")
        ]
        )
    
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']

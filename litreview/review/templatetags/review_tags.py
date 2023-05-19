from django import template
from django.db.models import Q
from review.models import Review

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def has_review(value):
    reviews = Review.objects.filter(Q(ticket=value) & ~Q(user=value.user))
    # print(value)
    return reviews

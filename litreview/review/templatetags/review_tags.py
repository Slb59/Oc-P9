from django import template
from review.models import Review

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def has_review(value):
    reviews = Review.objects.filter(ticket=value)
    # print(value)
    return reviews

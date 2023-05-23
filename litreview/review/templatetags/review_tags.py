from django import template
from django.db.models import Q
from review.models import Review

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def has_review(value):
    """ value = a ticket
    exist a review on the ticket from another user
    """
    reviews = Review.objects.filter(Q(ticket=value) & ~Q(user=value.user))
    return reviews


@register.filter
def my_review(value):
    """ value = a ticket
    exist a review on the ticket with same user
    """
    reviews = Review.objects.filter(Q(ticket=value) & Q(user=value.user))
    return reviews

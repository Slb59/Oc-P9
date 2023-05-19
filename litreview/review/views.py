from itertools import chain
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Value, BooleanField

from .models import Ticket, Review
from account.models import UserFollows
from .forms import TicketForm, ReviewForm


@login_required
def feed(request):
    """ display tickets and reviews """

    # users that the connected user follow
    user_follows = UserFollows.objects.filter(
        user=request.user).values_list('followed_user', flat=True)

    # reviews of connected user and user_follows
    reviews = Review.objects.filter(
        (Q(user=request.user) | Q(user__in=user_follows)))

    # exemple du cours avec Q :
    # blogs = models.Blog.objects.filter(
    #     Q(author__in=request.user.follows) | Q(starred=True))

    # tickets of connected user and users follows
    # without review => no
    tickets = Ticket.objects.filter(
        (Q(user=request.user) | Q(user__in=user_follows)))
    # ).exclude(review__in=reviews)
    
    # exemple avec exclude
    #     photos = models.Photo.objects.filter(
    #     uploader__in=request.user.follows.all()
    # ).exclude(blog__in=blogs)


    # comment distinguer les tickets avec une critique 
    # des tickets sans critique ??

    # reviews of conneted user and users follows
    # reviews = Review.objects.all()

    # tickets_with_review = []
    # for review in reviews:
    #     tickets_with_review.append(review.ticket)

    # merge tickets with review and tickets without review
    # tickets = chain(
    #     tickets_with_review.annotate(has_review=Value(True, BooleanField())),
    #     tickets_without_review.annotate(has_review=Value(False, BooleanField()))
    # )

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda x: x.time_created,
                                 reverse=True)

    # tickets_and_reviews = sorted(tickets,
    #                              key=lambda x: x.time_created,
    #                              reverse=True)

    # combine tickets and reviews
    # exemple du cours : 
    # blogs_and_photos = sorted(
    #     chain(blogs, photos),
    #     key=lambda instance: instance.date_created,
    #     reverse=True
    # )
    # context = {
    #     'blogs_and_photos': blogs_and_photos,
    # }
    # tickets_and_review = chain(reviews, tickets)
    # order by the posts by time_created desc

    context = {'tickets_and_reviews': tickets_and_reviews}

    return render(request, 'review/feed.html', context=context)


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    return render(request, 'review/ticket/ticket_info.html',
                  {'ticket': ticket
                   })


def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'review/ticket/list.html', {'tickets': tickets})


def ticket_list_user(request, id):
    user = get_object_or_404(User, id=id)
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'review/ticket/list_user.html',
                  {'tickets': tickets,
                   'user': user})


class ReviewView(LoginRequiredMixin, View):
    """ add a new review on ticket """
    ticket_form_class = TicketForm
    review_form_class = ReviewForm
    template_name = 'review/review/add_review.html'

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        context = {
            'ticket_form': ticket_form,
            'review_form': review_form,
        }
        return render(request,
                      self.template_name,
                      context=context)

    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)
        if ticket_form.is_valid():
            if review_form.is_valid():
                form_ticket = ticket_form.save(commit=False)
                form_ticket.user = request.user
                form_ticket.save()
                form = review_form.save(commit=False)
                form.ticket = form_ticket
                form.user = request.user
                form.save()
                return redirect(settings.LOGIN_REDIRECT_URL)


class ReviewOnTicketView(LoginRequiredMixin, View):
    """ add a new review on ticket """
    ...


class TicketView(LoginRequiredMixin, View):
    """ add a new ticket """
    form_class = TicketForm
    template_name = 'review/ticket/add_ticket.html'

    def get(self, request):
        form = self.form_class()
        return render(
            request, self.template_name,
            context={'ticket_form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

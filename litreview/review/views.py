from itertools import chain
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.views.generic.edit import DeleteView, UpdateView
# from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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

    # reviews of the connected user tickets
    tickets_user = Ticket.objects.filter(user=request.user)
    reviews_from_ticket_user = Review.objects.filter(
        ticket__in=tickets_user).exclude(pk__in=reviews)

    # tickets of connected user and users follows
    # without review => no
    tickets = Ticket.objects.filter(
        (Q(user=request.user) | Q(user__in=user_follows)))

    # merge tickets with review and tickets
    merge_tickets_and_reviews = chain(tickets, reviews)
    merge_tickets_and_reviews = chain(
        merge_tickets_and_reviews, reviews_from_ticket_user)

    # sorted the tickets and reviews by time created reverse               
    tickets_and_reviews = sorted(merge_tickets_and_reviews,
                                 key=lambda x: x.time_created,
                                 reverse=True)

    context = {'tickets_and_reviews': tickets_and_reviews}

    return render(request, 'review/feed.html', context=context)


@login_required
def posts(request):
    """ display tickets and reviews of the connected user """

    # reviews of connected user
    reviews = Review.objects.filter(user=request.user)

    # tickets of connected
    tickets = Ticket.objects.filter(user=request.user)

    # merge tickets with review and tickets
    merge_tickets_and_reviews = chain(tickets, reviews)

    # sorted the tickets and reviews by time created reverse               
    tickets_and_reviews = sorted(merge_tickets_and_reviews,
                                 key=lambda x: x.time_created,
                                 reverse=True)

    context = {'tickets_and_reviews': tickets_and_reviews}

    return render(request, 'review/posts.html', context=context)


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
    # model = Ticket
    review_form_class = ReviewForm
    template_name = 'review/review/add_review.html'

    def get(self, request, id_ticket):
        ticket = Ticket.objects.get(pk=id_ticket)
        form = self.review_form_class()
        context = {'review_form': form,
                   'ticket': ticket,
                   'no_add_review': True}
        return render(request,
                      'review/review/add_review_on_ticket.html',
                      context=context)

    def post(self, request, id_ticket):
        ticket = Ticket.objects.get(pk=id_ticket)
        review_form = self.review_form_class(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.ticket = ticket
            form.user = request.user
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)


class TicketView(LoginRequiredMixin, View):
    """ add a new ticket """
    form_class = TicketForm
    template_name = 'review/ticket/add_ticket.html'
    raise_exception = True

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


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    # fields = ['title', 'description', 'image']
    form_class = TicketForm
    template_name = 'review/ticket/ticket_update.html'
    success_url = '/posts'


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'review/ticket/ticket_confirm_delete.html'
    success_url = reverse_lazy('review:posts')


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    # fields = ['headline', 'body', 'rating']
    template_name = 'review/review/review_update.html'
    success_url = '/posts'


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'review/review/review_confirm_delete.html'
    success_url = reverse_lazy('review:posts')

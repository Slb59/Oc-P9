from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Ticket, Review
from account.models import UserFollows
from .forms import TicketForm


@login_required
def feed(request):
    """ display tickets and reviews """
    # reviews = Review.objects.all().order_by('-time_created')
    # Entry.objects.order_by(Coalesce('summary', 'headline').desc())

    # users that the connected user follow
    user_follows = UserFollows.objects.filter(user=request.user)
    users_filter = []
    users_filter.append(request.user)

    # tickets order by time_created desc
    # tickets of connected user and users follows
    # tickets = Ticket.objects.all().order_by('-time_created')
    # user_follows.followed_user
    tickets = Ticket.objects.filter(user__in=users_filter)

    # reviews of conneted user and users follows
    # reviews = Review.objects.all()

    # combine tickets and reviews

    # order by the posts by time_created desc

    return render(request, 'review/feed.html', {'tickets': tickets})


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    return render(request, 'review/ticket/ticket_info.html',
                  {'ticket': ticket})


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
    ...


class TicketView(LoginRequiredMixin, View):
    """ add a new ticket """
    form_class = TicketForm
    template_name = 'review/ticket/add_ticket.html'

    def get(self, request):
        form = self.form_class()
        return render(
            request, self.template_name,
            context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

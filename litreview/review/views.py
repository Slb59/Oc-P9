from django.shortcuts import render, get_object_or_404
from .models import Ticket


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    return render(request, 'review/ticket/detail.html', {'ticket': ticket})

def ticket_list(request):
    pass

# def ticket_list_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     tickets = Tickets.objects.filter(user=user)


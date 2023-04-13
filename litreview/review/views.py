from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Ticket


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    return render(request, 'review/ticket/detail.html', {'ticket': ticket})

def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request,'review/ticket/list.html',{'tickets': tickets})


def ticket_list_user(request, id):
    user = get_object_or_404(User, id=id)
    tickets = Ticket.objects.filter(user=user)
    return render(request,'review/ticket/list_user.html',{'tickets': tickets, 'user':user})


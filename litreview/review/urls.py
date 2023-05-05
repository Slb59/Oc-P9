from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
 path('', views.feed, name='feed'),
 path('tickets/', views.ticket_list, name='ticket_list'),
 path('tickets/<int:id>/', views.ticket_list_user, name='ticket_list_user'),
 path('ticket/<int:id>/', views.ticket_detail, name='ticket_detail'),
 path('add_ticket', views.TicketView.as_view(), name='add_ticket'),
]
from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
 path('tickets', views.ticket_list, name='ticket_list'),
 path('ticket/<int:id>/', views.ticket_detail, name='ticket_detail'),
]
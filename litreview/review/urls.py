from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
 path('<int:id>/', views.ticket_detail, name='ticket_detail'),
]
from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
 path('', views.feed, name='feed'),
 path('tickets/', views.ticket_list, name='ticket_list'),
 path('tickets/<int:id>/', views.ticket_list_user, name='ticket_list_user'),
 path('ticket/<int:id>/', views.ticket_detail, name='ticket_detail'),
 path('add_ticket', views.TicketView.as_view(), name='add_ticket'),
 path('add_review', views.ReviewView.as_view(), name='add_review'),
 path('add_review/<int:id_ticket>', views.ReviewOnTicketView.as_view(),
      name='add_review_on_ticket'),
 path('posts', views.posts, name='posts'),
 path('update_ticket/<pk>/', views.TicketUpdateView.as_view(),
      name='update_ticket'),
 path('delete_ticket/<pk>/', views.TicketDeleteView.as_view(),
      name='delete_ticket'),
 path('update_review/<pk>/', views.ReviewUpdateView.as_view(),
      name='update_review'),
 path('delete_review/<pk>/', views.ReviewDeleteView.as_view(),
      name='delete_review')
]

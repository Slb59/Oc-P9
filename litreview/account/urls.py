from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'account'

urlpatterns = [
 path('login/', views.LoginPage.as_view(), name='login'),
 path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
 path('signup/', views.signup, name='signup'),
 path('subscribe/', views.SubscriptionView.as_view(), name='subscription'),
 path('unsubscribe/<int:id>/', views.unsubscribe, name='unsubscription'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.registration, name="user-registration"),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='user-logout'),
    path('request/', views.request_send, name='request-send'),
    path('request-again/', views.request_send_again, name='request-send-again'),
    path('requests/', views.check_request, name='check-request')
]
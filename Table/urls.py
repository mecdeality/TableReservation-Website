from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='table-main'),
    path('restaurant/<int:restaurant_id>', views.restaurant, name='table-restaurant'),
    path('restaurant/<int:restaurant_id>/reserve/$', views.reserve, name='table-reserve'),
    path('reservations', views.reservations, name='table-reservations'),
    path('restaurants', views.admin_restaurants, name='admin-restaurants'),
    path('restaurants/<int:restaurant_id>', views.admin_reservations, name='admin-reservations'),
    path('restaurants/add', views.restaurant_add, name='restaurant-add')

]
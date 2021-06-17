from django.db import models
from django.contrib.auth.models import User
from datetime import date
from user.models import AccountType


# Create your models here.
class Restaurant(models.Model):
    preview_img = models.ImageField(null=True, blank=True, upload_to='images/preview')
    name = models.CharField(max_length=200)
    avg_check = models.IntegerField()
    cuisines = models.CharField(max_length=200)
    about = models.TextField()
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    account = models.ForeignKey(AccountType, on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return self.name


class RestaurantPicture(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True, upload_to=f'images/restaurant_pics/')


class Reservation(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=100)
    reserver = models.ForeignKey(User, on_delete=models.CASCADE)
    reserverName = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField(default=None)
    request = models.CharField(max_length=200, default='-')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    size = models.IntegerField(default=None)

    def __str__(self):
        return self.restaurant.name

    @property
    def is_past_due(self):
        return date.today() > self.date

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AccountType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurantAccount = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username+", Restaurant Account:"+ str(self.restaurantAccount)


class Request(models.Model):
    account = models.OneToOneField(AccountType, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    sendMsg = models.CharField(max_length=255, default='-')
    responseMsg = models.CharField(max_length=255, default='-')

    def __str__(self):
        return self.account.user.username
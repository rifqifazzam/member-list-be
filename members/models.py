from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CustomToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_expired(self):
        expiration_time = self.created_at + timedelta(minutes=1)
        return timezone.now() > expiration_time

    def __str__(self):
        return self.key








from django.db import models

# Create your models here.
class LoginPage(models.Model):
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
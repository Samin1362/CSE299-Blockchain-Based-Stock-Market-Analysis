from django.db import models

# Create your models here.
class LoginPage(models.Model):
    username = models.CharField(max_length=120)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.CharField(max_length=120, default=None)
    pass1 = models.CharField(max_length=120)
    pass2 = models.CharField(max_length=120)
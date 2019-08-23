from django.db import models

# Create your models here.

class Users(models.Model):
    userID = models.AutoField().primary_key
    emailAddress = models.EmailField(max_length = 50).unique
    password = models.CharField(max_length = 20)
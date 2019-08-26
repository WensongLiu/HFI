from django.db import models

# Create your models here.

class Users(models.Model):
    userID = models.AutoField(primary_key=True)
    emailAddress = models.EmailField(max_length = 50, unique=True)
    password = models.CharField(max_length = 20)
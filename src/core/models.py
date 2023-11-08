from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


# Recipes Model for DB
class Recipes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
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
    
# Extending User Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Avatars will require pillow, which has been added to requirements.txt
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
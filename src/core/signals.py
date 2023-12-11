# = = = = = = = = = = = = #
#        SDEV 265         #
#     Recipe Builder      #
# = = = = = = = = = = = = #
#       Aaron Corns       # 
#    Joseph Hollenbach    #
#     Reese McGuffey      #
#      Samuel Moore       #
# = = = = = = = = = = = = #
#       signals.py        #
# = = = = = = = = = = = = #

# Signals is only used with regards to user creation.
# Django is strict when it comes to users and we need to create
# a profile entry that will match the user so we can customize
# fields and features, such as photos and bios. When a user is 
# created a profile will also be created and linked.

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

# When a user creates a profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# When a user updates their profile
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

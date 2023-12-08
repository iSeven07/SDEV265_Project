from django.contrib import admin

from .models import Recipes, Profile

# Register your models here.
admin.site.register(Recipes)
admin.site.register(Profile)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipes

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

"""
class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = Recipes
        fields = ['title', 'content', 'ingredients']
"""

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipes
        fields = ['title', 'content']  # These are the fields you want to include in the form
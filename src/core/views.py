from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login
from .models import Recipes
from .forms import SignupForm

# Dummy Data
posts = [
    {
        'author': 'John Smith',
        'title': 'Recipe Post 1',
        'content': 'This is a recipe post',
        'date': '1 November 2023'
    },
    {
        'author': 'Jane Doe',
        'title': 'Recipe Post 2',
        'content': 'This is another recipe post',
        'date': '7 November 2023'
    }
]

# Home View
def home(request):
    print(request.headers)
    return render(request, "home.html", {'posts': Recipes.objects.all(), 'title': 'Home'})
    # return HttpResponse('<h1>Recipe Home</h1>')

# Search View
def search(request):
    print(request.headers)
    return render(request, "search.html", {'title': 'Search'})
    # return HttpResponse('<h1>Recipe Search</h1>')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe-home')
    else:
        form = SignupForm()
        return render(request, 'register.html', {'title': 'Register', 'form': form})
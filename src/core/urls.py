from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="recipe-home"),
    path('search/', views.search, name="recipe-search"),
    path('register/', views.register, name="recipe-register")
]
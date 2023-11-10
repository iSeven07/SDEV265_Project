from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="recipe-home"),
    path('search/', views.search, name="recipe-search"),
    path('register/', views.register, name="recipe-register"),
    path('submit_recipe/', views.submit_recipe, name='recipe-submit'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("profile/<str:username>/", views.user_profile, name='user-profile'),
] 